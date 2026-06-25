"""
Claude-Agent-SDK variant of the NL-assertions judge.

Does exactly the same work as `NLAssertionsEvaluator` — same system/user prompts,
same JSON parsing, same NLAssertionCheck output, no tools — but routes the single
judge LLM call through the Claude Agent SDK (subscription auth) instead of litellm.

Defaults to claude-opus-4-8 with "high" effort; both are configurable via the
class attributes below or the constants in tau2.config.
"""

from __future__ import annotations

from tau2.config import (
    DEFAULT_SDK_NL_ASSERTIONS_EFFORT,
    DEFAULT_SDK_NL_ASSERTIONS_MODEL,
)
from tau2.data_model.message import Message
from tau2.data_model.simulation import NLAssertionCheck
from tau2.evaluator.evaluator_nl_assertions import (
    FullDuplexNLAssertionsEvaluator,
    NLAssertionsEvaluator,
)
from tau2.utils.sdk_llm import generate_via_sdk


class SDKNLAssertionsEvaluator(NLAssertionsEvaluator):
    """NL-assertions judge backed by the Claude Agent SDK.

    Inherits calculate_reward and prompt/parse helpers from NLAssertionsEvaluator
    so the only thing that changes is the generation backend.
    """

    MODEL: str = DEFAULT_SDK_NL_ASSERTIONS_MODEL
    EFFORT: str = DEFAULT_SDK_NL_ASSERTIONS_EFFORT

    @classmethod
    def evaluate_nl_assertions(
        cls,
        trajectory: list[Message],
        nl_assertions: list[str],
    ) -> list[NLAssertionCheck]:
        """Same as the base evaluator, but the judge call goes through the SDK."""
        messages = cls.build_eval_messages(trajectory, nl_assertions)
        assistant_message = generate_via_sdk(
            model=cls.MODEL,
            messages=messages,
            effort=cls.EFFORT,
            call_name="nl_assertions_eval_sdk",
        )
        return cls.parse_nl_response(assistant_message.content)


class FullDuplexSDKNLAssertionsEvaluator(FullDuplexNLAssertionsEvaluator):
    """Full-duplex NL-assertions judge backed by the Claude Agent SDK."""

    @classmethod
    def evaluate_nl_assertions(
        cls,
        trajectory: list[Message],
        nl_assertions: list[str],
    ) -> list[NLAssertionCheck]:
        return SDKNLAssertionsEvaluator.evaluate_nl_assertions(
            trajectory, nl_assertions
        )
