"""
Claude-Agent-SDK backend for tau2's LLM judge.

This is a drop-in analog of `tau2.utils.llm_utils.generate` for the narrow case
the evaluator needs: a single-turn, no-tool, text-in/text-out completion. The only
difference vs. `generate` is the transport — instead of calling the provider
through litellm, it drives the Claude Agent SDK's bundled CLI, which authenticates
against the local Claude subscription (no API key required).

It is intentionally minimal: no streaming tool use, no multi-turn loop. tau2
messages map onto the SDK as:
  - SystemMessage(s) -> ClaudeAgentOptions.system_prompt (bare string replaces the
    CLI default, so the judge sees ONLY the evaluator's system prompt)
  - the remaining message(s) -> the single `query()` text
The SDK's final assistant text is returned as a tau2 AssistantMessage, mirroring
`generate`'s return type so callers (and downstream parsing) are unchanged.
"""

from __future__ import annotations

import asyncio
import os
import threading
import time
from typing import Any, Optional

from loguru import logger

from tau2.data_model.message import (
    AssistantMessage,
    Message,
    SystemMessage,
)

# Importing tau2 loads .env, which on subscription-only machines holds a PLACEHOLDER
# ANTHROPIC_API_KEY. The SDK subprocess inherits the parent env, and ANY
# ANTHROPIC_API_KEY -- even an invalid one -- overrides the subscription OAuth
# (apiKeySource becomes ANTHROPIC_API_KEY). Remove these in the parent process so the
# bundled CLI authenticates via the Claude subscription.
_AUTH_OVERRIDE_VARS = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_CUSTOM_HEADERS",
)
for _k in _AUTH_OVERRIDE_VARS:
    os.environ.pop(_k, None)

# Built-in Claude Code tools removed from the model's context. The judge needs no
# tools at all (parity with the litellm judge, which passes no tools); this is a
# hard guarantee that the bundled CLI cannot reach for Bash/Read/etc.
_DISALLOWED_BUILTINS = [
    "Task", "Bash", "BashOutput", "KillShell", "Edit", "Write", "Read",
    "NotebookEdit", "Glob", "Grep", "WebFetch", "WebSearch", "TodoWrite",
    "ExitPlanMode", "AskUserQuestion", "Skill", "ToolSearch",
]


def _clean_env() -> dict:
    """Env for the SDK subprocess: drop auth-override vars and this harness's own
    session vars so the subprocess starts from a clean, subscription-authed slate."""
    drop = set(_AUTH_OVERRIDE_VARS)
    return {
        k: v
        for k, v in os.environ.items()
        if k not in drop
        and not k.startswith("CLAUDE_CODE")
        and k not in ("CLAUDECODE", "CLAUDE_EFFORT")
    }


def _split_messages(messages: list[Message]) -> tuple[str, str]:
    """Map tau2 messages onto (system_prompt, query_text).

    System messages are concatenated into the SDK system prompt. All other messages
    are concatenated into the single query turn; when more than one non-system
    message is present they are role-labeled so context is preserved.
    """
    system_parts: list[str] = []
    other: list[Message] = []
    for m in messages:
        if isinstance(m, SystemMessage):
            if m.content:
                system_parts.append(m.content)
        else:
            other.append(m)

    if len(other) == 1:
        query_text = other[0].content or ""
    else:
        query_text = "\n\n".join(
            f"{m.role}: {m.content or ''}" for m in other
        )
    return "\n\n".join(system_parts), query_text


def _map_usage(usage: Any) -> Optional[dict]:
    """Map the SDK ResultMessage.usage onto tau2's {prompt_tokens, completion_tokens}."""
    if not usage:
        return None
    if not isinstance(usage, dict):
        usage = getattr(usage, "__dict__", None) or {}
    prompt = usage.get("input_tokens", usage.get("prompt_tokens", 0)) or 0
    completion = usage.get("output_tokens", usage.get("completion_tokens", 0)) or 0
    return {"prompt_tokens": int(prompt), "completion_tokens": int(completion)}


async def _generate_async(
    model: str,
    effort: str,
    system_prompt: str,
    query_text: str,
) -> dict:
    from claude_agent_sdk import ClaudeSDKClient

    options = build_sdk_options(model, system_prompt, effort)
    async with ClaudeSDKClient(options=options) as client:
        await client.query(query_text)
        return await _consume_turn(client)


def _run_async(coro) -> dict:
    """Run an async coroutine to completion from sync code, whether or not an event
    loop is already running in this thread (the evaluator is sync, but a caller may
    invoke it from within an async driver)."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    # A loop is already running in this thread: run the coroutine in a dedicated
    # thread with its own loop to avoid "loop already running" errors.
    result: dict = {}
    error: list[BaseException] = []

    def _worker() -> None:
        try:
            result.update(asyncio.run(coro))
        except BaseException as e:  # noqa: BLE001 - re-raised below
            error.append(e)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
    t.join()
    if error:
        raise error[0]
    return result


def build_sdk_options(
    model: str,
    system_prompt: str,
    effort: Optional[str] = None,
    mcp_servers: Optional[dict] = None,
    allowed_tools: Optional[list] = None,
):
    """Build ClaudeAgentOptions for a subscription-authed SDK chat.

    Shared by the single-shot judge, the persistent user-sim session, and (for
    tool-augmented users) an in-process MCP server. With no mcp_servers/allowed_tools
    this is the no-tool case (judge, standard user-sim).
    """
    from claude_agent_sdk import ClaudeAgentOptions

    options_kwargs: dict[str, Any] = dict(
        model=model,
        system_prompt=system_prompt,
        allowed_tools=list(allowed_tools) if allowed_tools else [],
        disallowed_tools=_DISALLOWED_BUILTINS,
        permission_mode="bypassPermissions",
        setting_sources=[],
        env=_clean_env(),
    )
    if effort:
        options_kwargs["effort"] = effort
    if mcp_servers:
        options_kwargs["mcp_servers"] = mcp_servers
    return ClaudeAgentOptions(**options_kwargs)


async def _consume_turn(client) -> dict:
    """Drive one SDK turn to completion; return final text + cost + usage.

    No-tool path: the user simulator (and judge) never call tools, so we only
    collect TextBlocks and the ResultMessage.
    """
    from claude_agent_sdk import (
        AssistantMessage as SDKAssistantMessage,
        ResultMessage,
        TextBlock,
    )

    text_parts: list[str] = []
    cost: Optional[float] = None
    usage: Any = None
    result_text: Optional[str] = None
    async for m in client.receive_response():
        if isinstance(m, SDKAssistantMessage):
            here = [b.text for b in m.content if isinstance(b, TextBlock)]
            if here:
                text_parts = here
        elif isinstance(m, ResultMessage):
            cost = m.total_cost_usd
            usage = m.usage
            result_text = m.result
    final_text = "".join(text_parts).strip() or (result_text or "").strip()
    return {"content": final_text, "cost": cost, "usage": _map_usage(usage)}


class SDKChatSession:
    """A persistent, sync-facing wrapper around a multi-turn ClaudeSDKClient.

    The SDK client is async and the CLI owns its own assistant turns (the query
    input stream only accepts user messages), so faithful multi-turn requires a
    LIVE client for the whole conversation rather than re-sending history each
    call. This class runs that client on a dedicated background event loop so sync
    tau2 code (e.g. the user simulator) can drive a true multi-turn SDK chat: each
    `send()` issues one user turn and the CLI retains all prior context.
    """

    def __init__(self, options):
        self._options = options
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._client = None
        self._started = False

    def _submit(self, coro):
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def start(self) -> None:
        if self._started:
            return
        from claude_agent_sdk import ClaudeSDKClient

        self._loop = asyncio.new_event_loop()

        def _runner() -> None:
            asyncio.set_event_loop(self._loop)
            self._loop.run_forever()

        self._thread = threading.Thread(target=_runner, daemon=True)
        self._thread.start()

        self._client = ClaudeSDKClient(options=self._options)
        self._submit(self._client.connect())
        self._started = True

    def send(self, text: str) -> dict:
        """Send one user turn; return {content, cost, usage} for the reply."""
        if not self._started:
            self.start()

        async def _turn() -> dict:
            await self._client.query(text)
            return await _consume_turn(self._client)

        return self._submit(_turn())

    def close(self) -> None:
        if not self._started:
            return
        try:
            self._submit(self._client.disconnect())
        except Exception as e:  # noqa: BLE001 - best-effort teardown
            logger.debug(f"SDKChatSession disconnect error: {e}")
        try:
            self._loop.call_soon_threadsafe(self._loop.stop)
            if self._thread is not None:
                self._thread.join(timeout=5)
        except Exception as e:  # noqa: BLE001
            logger.debug(f"SDKChatSession loop teardown error: {e}")
        self._started = False


def generate_via_sdk(
    model: str,
    messages: list[Message],
    effort: str = "high",
    call_name: Optional[str] = None,
    **kwargs: Any,
) -> AssistantMessage:
    """
    Generate a response via the Claude Agent SDK (subscription auth, no tools).

    Mirrors `tau2.utils.llm_utils.generate`'s signature and return type for the
    single-turn, no-tool judge use case. `effort` is the SDK reasoning-effort knob
    ("low"|"medium"|"high"|"max"). Extra kwargs accepted from the litellm signature
    (e.g. temperature, num_retries) are ignored — the SDK does not take them.

    Args:
        model: SDK model id (e.g. "claude-opus-4-8").
        messages: tau2 messages (system + user) to send.
        effort: SDK reasoning effort level.
        call_name: Optional label for debug logging.
        **kwargs: Ignored (litellm-compat).

    Returns:
        AssistantMessage with the model's final text, cost, and usage.
    """
    system_prompt, query_text = _split_messages(messages)
    start = time.perf_counter()
    out = _run_async(_generate_async(model, effort, system_prompt, query_text))
    generation_time_seconds = time.perf_counter() - start

    message = AssistantMessage(
        role="assistant",
        content=out["content"],
        tool_calls=None,
        cost=out.get("cost"),
        usage=out.get("usage"),
        generation_time_seconds=generation_time_seconds,
    )
    if call_name:
        logger.debug(
            f"[sdk_llm:{call_name}] model={model} effort={effort} "
            f"cost={out.get('cost')} time={generation_time_seconds:.1f}s"
        )
    return message
