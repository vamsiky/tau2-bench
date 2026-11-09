"""Tests for the verified DB comparison (use_verified_scorer=True).

Uses task_060 (open a savings account, then close a $0 checking account). The gold
closes the account without a reason, so closure_reason gets the tool's default.
"""

import json

import pytest

from tau2.data_model.message import AssistantMessage, ToolCall
from tau2.domains.banking_knowledge.environment import get_db
from tau2.domains.banking_knowledge.tools import KnowledgeTools, KnowledgeUserTools
from tau2.environment.environment import Environment
from tau2.evaluator.evaluator_env import EnvironmentEvaluator, _verified_db_match
from tau2.runner import get_tasks
from tau2.runner.build import _derive_read_log_allowlist

ORDER_CARD = "order_debit_card_5739"
CLOSED_ACCOUNT = "58d57780cc15e32d"
# Valid in form; rejected because the gold closes this account first.
ORDER = {
    "account_id": CLOSED_ACCOUNT,
    "user_id": "jm60a8b9c2",
    "delivery_option": "STANDARD",
    "delivery_fee": 0,
    "card_design": "CLASSIC",
    "design_fee": 0,
    "shipping_address": "4521 Mountain View Drive, Denver, CO 80202",
}
BAD_INPUT_ORDER = {**ORDER, "delivery_option": "OVERNIGHT"}


@pytest.fixture(scope="module")
def task():
    return get_tasks("banking_knowledge", task_ids=["task_060"])[0]


def _env_constructor(task):
    allowlist = _derive_read_log_allowlist(task)

    def constructor(solo_mode: bool = False) -> Environment:
        tools = KnowledgeTools(get_db())
        tools.set_read_log_allowlist(allowlist)
        return Environment(
            domain_name="banking_knowledge",
            policy="",
            tools=tools,
            user_tools=KnowledgeUserTools(tools.db),
        )

    return constructor


def _gold_calls(task) -> list[tuple[str, dict]]:
    return [(a.name, dict(a.arguments)) for a in task.evaluation_criteria.actions]


def _discoverable(name: str, args: dict) -> list[tuple[str, dict]]:
    return [
        ("unlock_discoverable_agent_tool", {"agent_tool_name": name}),
        (
            "call_discoverable_agent_tool",
            {"agent_tool_name": name, "arguments": json.dumps(args)},
        ),
    ]


def _trajectory(task, calls):
    """Run the calls on a live environment and record them as messages."""
    env = _env_constructor(task)()
    init = task.initial_state
    env.set_state(
        initialization_data=init.initialization_data,
        initialization_actions=init.initialization_actions,
        message_history=[],
    )
    messages = list(init.message_history or [])
    for i, (name, args) in enumerate(calls):
        tool_call = ToolCall(id=f"call_{i}", name=name, arguments=args)
        messages.append(AssistantMessage.text("", tool_calls=[tool_call]))
        messages.append(env.get_response(tool_call))
    return messages


def _rewards(task, calls) -> tuple[float, float]:
    """(strict reward, verified reward) for a trajectory made of these calls."""
    messages = _trajectory(task, calls)
    return tuple(
        EnvironmentEvaluator.calculate_reward(
            environment_constructor=_env_constructor(task),
            task=task,
            full_trajectory=messages,
            use_verified_scorer=verified,
        ).reward
        for verified in (False, True)
    )


def test_gold_passes_both(task):
    assert _rewards(task, _gold_calls(task)) == (1.0, 1.0)


def test_bank_account_closure_reason_ignored(task):
    calls = _gold_calls(task)
    name, args = calls[-1]
    inner = json.loads(args["arguments"])
    assert inner == {"account_id": CLOSED_ACCOUNT}
    inner["reason"] = "Moving to another bank"
    calls[-1] = (name, {**args, "arguments": json.dumps(inner)})
    assert _rewards(task, calls) == (0.0, 1.0)


def test_extra_write_rejected_for_bad_input_allowed(task):
    calls = _gold_calls(task) + _discoverable(ORDER_CARD, BAD_INPUT_ORDER)
    messages = _trajectory(task, calls)
    assert messages[-1].content.startswith("Error: Invalid delivery_option")
    assert _rewards(task, calls) == (0.0, 1.0)


def test_extra_write_rejected_by_policy_fails(task):
    calls = _gold_calls(task) + _discoverable(ORDER_CARD, ORDER)
    messages = _trajectory(task, calls)
    assert messages[-1].content.startswith("Error: Account must be OPEN")
    assert _rewards(task, calls) == (0.0, 0.0)


def test_extra_write_with_input_error_then_policy_rejection_fails(task):
    calls = (
        _gold_calls(task)
        + _discoverable(ORDER_CARD, BAD_INPUT_ORDER)
        + _discoverable(ORDER_CARD, ORDER)
    )
    assert _rewards(task, calls) == (0.0, 0.0)


def test_missing_required_discoverable_call_fails(task):
    calls = [
        call
        for call in _gold_calls(task)
        if call[1].get("agent_tool_name") != "get_all_user_accounts_by_user_id_3847"
    ]
    assert _rewards(task, calls) == (0.0, 0.0)


def _db(table: str, record: dict) -> dict:
    return {table: {"data": {"r1": record}}}


def test_card_closure_reasons_compared():
    for table in ("debit_cards", "credit_card_closure_reasons"):
        gold = _db(table, {"status": "CLOSED", "closure_reason": "lost"})
        predicted = _db(table, {"status": "CLOSED", "closure_reason": "stolen"})
        assert _verified_db_match(gold, predicted)[0] is False


def test_account_closure_reason_ignored():
    gold = _db("accounts", {"status": "CLOSED", "closure_reason": "default"})
    predicted = _db("accounts", {"status": "CLOSED", "closure_reason": "moving"})
    assert _verified_db_match(gold, predicted)[0] is True


def test_extra_reads_allowed(task):
    calls = (
        _gold_calls(task)
        # A read the gold never calls, and a repeat of one it does.
        + _discoverable(
            "get_debit_cards_by_account_id_7823", {"account_id": "38a2c5f77504be6c"}
        )
        + _discoverable(
            "get_all_user_accounts_by_user_id_3847", {"user_id": "jm60a8b9c2"}
        )
    )
    messages = _trajectory(task, calls)
    assert not messages[-3].content.startswith("Error")
    assert _rewards(task, calls) == (1.0, 1.0)
