"""
Claude-Agent-SDK variant of the tau2 user simulator.

Does the same work as `UserSimulator` — same global simulation guidelines, same
scenario/persona system prompt, same UserMessage output and stop-token semantics —
but routes generation through the Claude Agent SDK (subscription auth, no API key)
instead of litellm. Defaults to claude-opus-4-8 with "high" effort; both are
configurable (via the model passed as `llm`, the `effort` key in `llm_args`, or the
class attributes / config constants).

Fidelity note: the SDK CLI owns its own assistant turns (its query input stream only
accepts user messages), so a faithful multi-turn conversation needs a LIVE client
for the whole episode rather than re-sending the flipped history each call (as the
litellm path does). This simulator therefore holds a persistent `SDKChatSession` and
sends only the newest agent utterance each turn; the CLI retains all prior context,
which is equivalent to the litellm path's full-history re-send.

User-side tools (e.g. banking_knowledge: apply_for_credit_card, submit_transaction):
the env's user tools are bridged as in-process MCP tools that execute against the
SAME environment (requestor="user"), exactly like the agent-side bridge. The SDK
session owns the inner tool loop; each user tool call is captured (ToolCall +
ToolMessage, ids matched) and exposed via `last_turn_tool_messages` so the driver
records them into the trajectory before the turn's final spoken message. Because the
SDK owns tool execution, this only works in the custom driver (not under `tau2 run`,
whose orchestrator expects to execute the user's tool calls itself) — the same
constraint as the SDK agent. The driver must call `bind_environment(env)` before use.
"""

from __future__ import annotations

import asyncio
import uuid
from typing import Optional

from loguru import logger

from tau2.config import DEFAULT_SDK_USER_EFFORT, DEFAULT_SDK_USER_MODEL
from tau2.data_model.message import (
    AssistantMessage,
    Message,
    MultiToolMessage,
    ToolCall,
    ToolMessage,
    UserMessage,
)
from tau2.data_model.persona import PersonaConfig
from tau2.environment.tool import Tool
from tau2.user.user_simulator import UserSimulator
from tau2.user.user_simulator_base import (
    OUT_OF_SCOPE,
    STOP,
    TRANSFER,
    UserState,
    ValidUserInputMessage,
)
from tau2.utils.sdk_llm import SDKChatSession, build_sdk_options

_USER_MCP_SERVER = "user_env"

# Shared instruction tail: the bundled CLI should behave like a raw chat completion
# for its SPOKEN turns (only the customer's next utterance, plain text), and use the
# same stop tokens UserSimulator.is_stop already checks for.
_SPEECH_RULES = (
    "Your spoken replies to the agent must be ONLY the customer's next message as "
    "plain text — no preamble, no role labels, no quotation marks, no markdown. "
    "Follow the conversation guidelines above for when to end the conversation, "
    f"emitting {STOP}, {TRANSFER}, or {OUT_OF_SCOPE} exactly as instructed there."
)

# No-tool case: forbid tool use entirely.
_USER_OUTPUT_SUFFIX = (
    "\n\nIMPORTANT: You ARE the customer. Do not use any tools. " + _SPEECH_RULES
)

# Tool-augmented case: the customer MAY use their own tools to take actions.
_USER_OUTPUT_SUFFIX_TOOLS = (
    "\n\nIMPORTANT: You ARE the customer. You may call your available tools to take "
    "the actions described in the guidelines/scenario (e.g. applying for a product). "
    "After any tool use, speak to the agent. " + _SPEECH_RULES
)


class SDKUserSimulator(UserSimulator):
    """User simulator backed by a persistent Claude Agent SDK session."""

    DEFAULT_MODEL: str = DEFAULT_SDK_USER_MODEL
    DEFAULT_EFFORT: str = DEFAULT_SDK_USER_EFFORT

    def __init__(
        self,
        llm: Optional[str] = None,
        instructions: Optional[str] = None,
        tools: Optional[list[Tool]] = None,
        llm_args: Optional[dict] = None,
        persona_config: Optional[PersonaConfig] = None,
    ):
        super().__init__(
            instructions=instructions,
            tools=tools,
            llm=llm,
            llm_args=llm_args,
            persona_config=persona_config,
        )
        self._sdk_model = self._resolve_model(llm)
        args = llm_args or {}
        self._sdk_effort = args.get("effort", self.DEFAULT_EFFORT)
        self._session: Optional[SDKChatSession] = None
        # Environment for executing user tools; bound by the driver before use.
        self._env = None
        # Per-turn capture of (ToolCall, ToolMessage) for user tool calls, and the
        # trajectory messages built from them for the most recent turn.
        self._captures: list[tuple[ToolCall, ToolMessage]] = []
        self._tool_lock: Optional[asyncio.Lock] = None
        self.last_turn_tool_messages: list[Message] = []

    @classmethod
    def _resolve_model(cls, llm: Optional[str]) -> str:
        """Use the passed model if it is an SDK/Claude model; otherwise default to
        the configured opus model (the framework default `llm` is gpt-4.1, which is
        meaningless for the SDK backend)."""
        if llm and ("claude" in llm or llm in {"opus", "sonnet", "haiku"}):
            return llm
        return cls.DEFAULT_MODEL

    def bind_environment(self, env) -> None:
        """Bind the environment whose user tools this simulator executes. Required
        before the first turn when the user has tools (no-op otherwise)."""
        self._env = env

    def _make_user_tool(self, tau2_tool: Tool):
        """Bridge one tau2 user Tool as an in-process SDK MCP tool that executes
        against the bound environment (requestor='user') and records the call."""
        from claude_agent_sdk import tool

        name = tau2_tool.name
        fn = tau2_tool.openai_schema["function"]
        description = fn.get("description") or name
        input_schema = fn["parameters"]

        @tool(name, description, input_schema)
        async def _handler(args: dict) -> dict:
            tc = ToolCall(
                id=uuid.uuid4().hex,
                name=name,
                arguments=dict(args),
                requestor="user",
            )
            async with self._tool_lock:
                tool_msg = await asyncio.to_thread(self._env.get_response, tc)
            self._captures.append((tc, tool_msg))
            text = tool_msg.content if tool_msg.content is not None else ""
            return {
                "content": [{"type": "text", "text": text}],
                "is_error": bool(tool_msg.error),
            }

        return _handler

    def _build_user_tool_server(self):
        from claude_agent_sdk import create_sdk_mcp_server

        sdk_tools = [self._make_user_tool(t) for t in self.tools]
        return create_sdk_mcp_server(
            name=_USER_MCP_SERVER, version="1.0.0", tools=sdk_tools
        )

    def _get_session(self) -> SDKChatSession:
        if self._session is None:
            mcp_servers = None
            allowed_tools = None
            suffix = _USER_OUTPUT_SUFFIX
            if self.tools:
                if self._env is None:
                    raise RuntimeError(
                        "SDKUserSimulator has user tools but no environment is bound. "
                        "Call bind_environment(env) before generating messages."
                    )
                self._tool_lock = asyncio.Lock()
                mcp_servers = {_USER_MCP_SERVER: self._build_user_tool_server()}
                allowed_tools = [f"mcp__{_USER_MCP_SERVER}__{t.name}" for t in self.tools]
                suffix = _USER_OUTPUT_SUFFIX_TOOLS

            options = build_sdk_options(
                model=self._sdk_model,
                system_prompt=self.system_prompt + suffix,
                effort=self._sdk_effort,
                mcp_servers=mcp_servers,
                allowed_tools=allowed_tools,
            )
            self._session = SDKChatSession(options)
            self._session.start()
            logger.debug(
                f"SDKUserSimulator session started: model={self._sdk_model} "
                f"effort={self._sdk_effort} user_tools={len(self.tools or [])}"
            )
        return self._session

    def set_seed(self, seed: int) -> None:
        """The SDK backend has no seed control; record it but no-op."""
        self.seed = seed

    def _generate_next_message(
        self, message: ValidUserInputMessage, state: UserState
    ) -> UserMessage:
        if isinstance(message, AssistantMessage) and message.is_audio:
            raise ValueError(
                "Assistant message cannot be audio. Use VoiceUserSimulator instead."
            )
        logger.debug(f"User (SDK) responds to message: {message}")

        # State bookkeeping identical to the base simulator so the trajectory the
        # orchestrator assembles is unchanged.
        if isinstance(message, MultiToolMessage):
            state.messages.extend(message.tool_messages)
        elif isinstance(message, ToolMessage):
            state.messages.append(message)
        elif message.has_content() or message.is_tool_call():
            state.messages.append(message)

        # Send only the newest agent utterance; the persistent session retains the
        # full prior conversation (server-side). User tool calls (if any) execute
        # inside the session and land in self._captures.
        self._captures = []
        agent_text = message.content if message.content else "(no content)"
        out = self._get_session().send(agent_text)

        # Turn the captured user tool calls into trajectory messages (ids matched, so
        # the evaluator's replay accepts them). Each call is its own UserMessage
        # (tool_calls) immediately followed by its ToolMessage, in execution order.
        tool_msgs: list[Message] = []
        for tc, tm in self._captures:
            tool_msgs.append(
                UserMessage(role="user", tool_calls=[tc], cost=0.0)
            )
            tool_msgs.append(
                ToolMessage(
                    id=tc.id,
                    role="tool",
                    content=tm.content,
                    requestor="user",
                    error=bool(tm.error),
                )
            )
        self.last_turn_tool_messages = tool_msgs

        user_response = out["content"]
        logger.debug(f"Response (SDK): {user_response}")
        return UserMessage(
            role="user",
            content=user_response,
            cost=out.get("cost"),
            usage=out.get("usage"),
        )

    def close(self) -> None:
        """Tear down the persistent SDK session (and its CLI subprocess)."""
        if self._session is not None:
            self._session.close()
            self._session = None

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass
