import copy
import re
from typing import Callable

from loguru import logger

from tau2.data_model.message import (
    AssistantMessage,
    Message,
    MultiToolMessage,
    Tick,
    ToolMessage,
    UserMessage,
)
from tau2.data_model.simulation import DBCheck, EnvAssertionCheck, RewardInfo
from tau2.data_model.tasks import RewardType, Task
from tau2.environment.environment import Environment
from tau2.evaluator.evaluator_base import EvaluatorBase

# Free-text annotation fields that carry no functional state and are excluded
# from the verified DB comparison (SABER "τ-Bench Verified" style), per table.
# Only bank-account closures qualify: close_bank_account_7392 takes an optional
# free-text reason with a hidden default. Debit-card and credit-card closure
# reasons are fixed categories the policy asks the agent to choose, so they
# are compared like any other field.
_FREE_TEXT_ANNOTATION_FIELDS: dict[str, frozenset[str]] = {
    "accounts": frozenset({"closure_reason"}),
}

# Tool results that reject a call for malformed input (missing, mistyped, or
# out-of-range arguments, or an ID that does not exist) before any state change.
# Rejections for status, eligibility, balance, ownership, or duplicates are not
# input errors: they block an action the policy forbids.
_INPUT_ERROR_RE = re.compile(
    r"^Error: (?:Missing required parameter|Invalid |Unexpected parameter|"
    r".*(?: is required| are required|must be (?:a number|numbers|an integer|"
    r"positive|a positive|a whole number|exactly \d+ digits)|PIN cannot be"
    r"| not found\.))"
)


def _strip_free_text(db: dict) -> dict:
    db = copy.deepcopy(db)
    for table_name, fields in _FREE_TEXT_ANNOTATION_FIELDS.items():
        table = db.get(table_name)
        data = table.get("data") if isinstance(table, dict) else None
        if isinstance(data, dict):
            for rec in data.values():
                if isinstance(rec, dict):
                    for field in fields:
                        rec.pop(field, None)
    return db


def _input_rejected_discoverable_tools(messages: list[Message]) -> set[str]:
    """Names of agent discoverable tools whose every call was rejected for bad input.

    Such a call changes nothing but still logs a row in agent_discoverable_tools,
    e.g. when the agent tries a tool variant with malformed arguments and then
    switches to the right one.
    """
    results = {}
    for message in messages:
        tool_messages = (
            message.tool_messages
            if isinstance(message, MultiToolMessage)
            else [message]
            if isinstance(message, ToolMessage)
            else []
        )
        for tm in tool_messages:
            results[tm.id] = tm.content or ""

    outcomes: dict[str, bool] = {}
    for message in messages:
        if not isinstance(message, AssistantMessage) or not message.tool_calls:
            continue
        for tc in message.tool_calls:
            if tc.name != "call_discoverable_agent_tool":
                continue
            name = tc.arguments.get("agent_tool_name")
            rejected = bool(_INPUT_ERROR_RE.match(results.get(tc.id, "")))
            outcomes[name] = outcomes.get(name, True) and rejected
    return {name for name, rejected in outcomes.items() if rejected}


def _verified_db_match(
    gold_db: dict,
    predicted_db: dict,
    input_rejected_tools: set[str] = frozenset(),
) -> tuple[bool, list[str]]:
    """
    Principled relaxed DB comparison (SABER "τ-Bench Verified" style).

    Two relaxations vs. exact hash match:
    1. agent_discoverable_tools — gold's called tool_names must be a SUBSET of
       the agent's (missing a required call still fails). An extra tool name is
       allowed only if every call to it was rejected for bad input
       (input_rejected_tools); any other extra call fails.
    2. Free-text annotation fields (bank-account closure_reason) are stripped
       before comparing (a descriptive value is equivalent to the default).

    All other tables are still compared exactly.
    Returns (match: bool, reasons: list[str]).
    """
    gold_db = _strip_free_text(gold_db)
    predicted_db = _strip_free_text(predicted_db)
    reasons: list[str] = []

    def _tool_names(db: dict) -> set:
        return {
            r.get("tool_name")
            for r in (
                db.get("agent_discoverable_tools", {}).get("data", {}) or {}
            ).values()
        }

    gold_tools = _tool_names(gold_db)
    predicted_tools = _tool_names(predicted_db)
    missing = gold_tools - predicted_tools
    if missing:
        reasons.append(f"missing required discoverable calls: {sorted(missing)}")
    extra = predicted_tools - gold_tools - set(input_rejected_tools)
    if extra:
        reasons.append(f"extra discoverable calls: {sorted(extra)}")

    for table in sorted(set(gold_db) | set(predicted_db)):
        if table == "agent_discoverable_tools":
            continue
        if gold_db.get(table) != predicted_db.get(table):
            reasons.append(f"table '{table}' differs")

    return len(reasons) == 0, reasons


class EnvironmentEvaluator(EvaluatorBase[Message]):
    """
    Evaluator focuses on endstate of the simulation environment.
    """

    @classmethod
    def calculate_reward(
        cls,
        environment_constructor: Callable[[], Environment],
        task: Task,
        full_trajectory: list[
            Message
        ],  # FIXME: It would be better to be able to get only the messages that are after the initial state
        solo_mode: bool = False,
        env_kwargs: dict = None,
        strict_replay: bool = True,
        use_verified_scorer: bool = False,
    ) -> RewardInfo:
        """
        Calculate the reward for the simulation.
        Args:
            environment_constructor: Callable[[], Environment]
            task: Task
            full_trajectory: list[Message] (Must include the message history from task initial state)
            solo_mode: bool
            strict_replay: forwarded to Environment.set_state(strict=...). Set
                False when re-grading historical trajectories whose recorded
                tool outputs may cosmetically differ from current tool code.
            use_verified_scorer: If True, replace the exact DB-hash comparison with the
                principled "tau2 Verified" relaxation: gold's discoverable calls must be a
                subset of the agent's, extra ones are allowed only if every call to them
                was rejected for bad input, and bank-account closure_reason is excluded.
                All other tables are still compared exactly.
        Returns:
            RewardInfo
        """
        if task.evaluation_criteria is None:
            return RewardInfo(
                reward=1.0,
                info={"note": "No evaluation criteria"},
            )
        expected_actions = task.evaluation_criteria.actions
        env_assertions = task.evaluation_criteria.env_assertions
        if expected_actions is None and env_assertions is None:
            return RewardInfo(
                reward=1.0,
                db_check=DBCheck(db_match=True, db_reward=1.0),
                info={"note": "No expected actions or env assertions"},
            )

        initialization_data = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_data is not None
        ):
            initialization_data = task.initial_state.initialization_data

        initialization_actions = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_actions is not None
        ):
            initialization_actions = task.initial_state.initialization_actions

        message_history = []
        if (
            task.initial_state is not None
            and task.initial_state.message_history is not None
        ):
            message_history = task.initial_state.message_history

        if env_kwargs is None:
            env_kwargs = {}

        predicted_environment = environment_constructor(
            solo_mode=solo_mode, **env_kwargs
        )

        predicted_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=list(full_trajectory),
            strict=strict_replay,
        )

        # Setting up gold environment
        gold_environment = environment_constructor(**env_kwargs)
        gold_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=message_history,
            strict=strict_replay,
        )
        golden_actions = task.evaluation_criteria.actions or []
        for action in golden_actions:
            try:
                gold_environment.make_tool_call(
                    tool_name=action.name,
                    requestor=action.requestor,
                    **action.arguments,
                )
            except Exception as e:
                logger.warning(
                    f"Error in golden actions {action.name}({action.arguments}): {e}"
                )

        # Comparing the environments
        if (
            use_verified_scorer
            and hasattr(gold_environment, "tools")
            and gold_environment.tools is not None
            and hasattr(gold_environment.tools, "db")
            and gold_environment.tools.db is not None
        ):
            gold_db = gold_environment.tools.db.model_dump()
            predicted_db = predicted_environment.tools.db.model_dump()
            input_rejected = _input_rejected_discoverable_tools(full_trajectory)
            agent_db_match, _ = _verified_db_match(
                gold_db, predicted_db, input_rejected
            )
            # Apply the same relaxed comparison for user_db. In domains where
            # user_tools.db is the same object as tools.db (e.g. banking), the exact
            # hash would undo the agent_discoverable_tools relaxation above.
            if (
                gold_environment.user_tools is not None
                and gold_environment.user_tools.db is not None
            ):
                gold_user_db = gold_environment.user_tools.db.model_dump()
                predicted_user_db = predicted_environment.user_tools.db.model_dump()
                user_db_match, _ = _verified_db_match(
                    gold_user_db, predicted_user_db, input_rejected
                )
            else:
                user_db_match = (
                    gold_environment.get_user_db_hash()
                    == predicted_environment.get_user_db_hash()
                )
        else:
            agent_db_match = (
                gold_environment.get_db_hash() == predicted_environment.get_db_hash()
            )
            user_db_match = (
                gold_environment.get_user_db_hash()
                == predicted_environment.get_user_db_hash()
            )

        if agent_db_match and user_db_match:
            db_reward = 1.0
            db_match = True
        else:
            db_reward = 0.0
            db_match = False

        db_check = DBCheck(db_match=db_match, db_reward=db_reward)

        # Run env assertions
        env_assertions = task.evaluation_criteria.env_assertions or []
        env_assertion_checks = []
        env_assertion_reward = 1.0
        for env_assertion in env_assertions:
            success = predicted_environment.run_env_assertion(
                env_assertion,
                raise_assertion_error=False,
            )
            res = EnvAssertionCheck(
                env_assertion=env_assertion,
                met=success,
                reward=1.0 if success else 0.0,
            )
            env_assertion_checks.append(res)
            env_assertion_reward *= res.reward

        reward = 1.0
        reward_breakdown = {}
        if RewardType.DB in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.DB] = db_reward
            reward *= db_reward
        if RewardType.ENV_ASSERTION in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.ENV_ASSERTION] = env_assertion_reward
            reward *= env_assertion_reward

        return RewardInfo(
            reward=reward,
            db_check=db_check,
            env_assertions=env_assertion_checks,
            reward_basis=task.evaluation_criteria.reward_basis,
            reward_breakdown=reward_breakdown,
        )


class FullDuplexEnvironmentEvaluator(EvaluatorBase[Tick]):
    """
    Evaluator focuses on endstate of the simulation environment.
    """

    @classmethod
    def ticks_to_message_history(cls, ticks: list[Tick]) -> list[Message]:
        """
        Convert a list of Ticks to a message history suitable for Environment.set_state().

        The order follows the execution order in FullDuplexOrchestrator:
        - User tool calls are processed before agent tool calls within each tick
        - Each tool call message is followed by its corresponding tool results

        Args:
            ticks: List of Tick objects from full-duplex simulation.

        Returns:
            List of Messages in the format expected by Environment.set_state():
            [UserMessage with tool_calls, ToolMessage results, AssistantMessage with tool_calls, ToolMessage results, ...]
        """
        messages: list[Message] = []

        for tick in ticks:
            # 1. User tool calls first (processed before agent in orchestrator)
            if tick.user_tool_calls:
                user_msg = UserMessage(
                    role="user",
                    content=tick.user_chunk.content if tick.user_chunk else None,
                    tool_calls=tick.user_tool_calls,
                    timestamp=(
                        tick.user_chunk.timestamp if tick.user_chunk else tick.timestamp
                    ),
                    contains_speech=(
                        tick.user_chunk.contains_speech if tick.user_chunk else False
                    ),
                )
                messages.append(user_msg)
                messages.extend(tick.user_tool_results)

            # 2. Agent tool calls second
            if tick.agent_tool_calls:
                agent_msg = AssistantMessage(
                    role="assistant",
                    content=tick.agent_chunk.content if tick.agent_chunk else None,
                    tool_calls=tick.agent_tool_calls,
                    timestamp=(
                        tick.agent_chunk.timestamp
                        if tick.agent_chunk
                        else tick.timestamp
                    ),
                    contains_speech=(
                        tick.agent_chunk.contains_speech if tick.agent_chunk else False
                    ),
                )
                messages.append(agent_msg)
                messages.extend(tick.agent_tool_results)

        return messages

    @classmethod
    def calculate_reward(
        cls,
        environment_constructor: Callable[[], Environment],
        task: Task,
        full_trajectory: list[Tick],
        solo_mode: bool = False,
        env_kwargs: dict = None,
        strict_replay: bool = True,
        use_verified_scorer: bool = False,
    ) -> RewardInfo:
        """
        Calculate the reward for the simulation.
        Args:
            environment_constructor: Callable[[], Environment]
            task: Task
            full_trajectory: list[Tick]
            solo_mode: bool
            env_kwargs: dict
            strict_replay: forwarded to Environment.set_state(strict=...). Set
                False when re-grading historical trajectories whose recorded
                tool outputs may cosmetically differ from current tool code.
            use_verified_scorer: If True, replace the exact DB-hash comparison with the
                principled "tau2 Verified" relaxation. See EnvironmentEvaluator for details.
        Returns:
            RewardInfo
        """
        if env_kwargs is None:
            env_kwargs = {}
        if task.evaluation_criteria is None:
            return RewardInfo(
                reward=1.0,
                info={"note": "No evaluation criteria"},
            )
        expected_actions = task.evaluation_criteria.actions
        env_assertions = task.evaluation_criteria.env_assertions
        if expected_actions is None and env_assertions is None:
            return RewardInfo(
                reward=1.0,
                db_check=DBCheck(db_match=True, db_reward=1.0),
                info={"note": "No expected actions or env assertions"},
            )

        initialization_data = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_data is not None
        ):
            initialization_data = task.initial_state.initialization_data

        initialization_actions = None
        if (
            task.initial_state is not None
            and task.initial_state.initialization_actions is not None
        ):
            initialization_actions = task.initial_state.initialization_actions

        message_history = []
        if (
            task.initial_state is not None
            and task.initial_state.message_history is not None
        ):
            message_history = task.initial_state.message_history

        # Convert ticks to message history for set_state
        # Note: Audio native does not support task history, so we only use the simulation trajectory
        predicted_message_history = cls.ticks_to_message_history(full_trajectory)

        predicted_environment = environment_constructor(
            solo_mode=solo_mode, **env_kwargs
        )
        predicted_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=predicted_message_history,
            strict=strict_replay,
        )

        # Setting up gold environment
        gold_environment = environment_constructor(**env_kwargs)
        gold_environment.set_state(
            initialization_data=initialization_data,
            initialization_actions=initialization_actions,
            message_history=message_history,
            strict=strict_replay,
        )
        golden_actions = task.evaluation_criteria.actions or []
        for action in golden_actions:
            try:
                gold_environment.make_tool_call(
                    tool_name=action.name,
                    requestor=action.requestor,
                    **action.arguments,
                )
            except Exception as e:
                logger.warning(
                    f"Error in golden actions {action.name}({action.arguments}): {e}"
                )

        # Comparing the environments
        if (
            use_verified_scorer
            and hasattr(gold_environment, "tools")
            and gold_environment.tools is not None
            and hasattr(gold_environment.tools, "db")
            and gold_environment.tools.db is not None
        ):
            gold_db = gold_environment.tools.db.model_dump()
            predicted_db = predicted_environment.tools.db.model_dump()
            input_rejected = _input_rejected_discoverable_tools(
                predicted_message_history
            )
            agent_db_match, _ = _verified_db_match(
                gold_db, predicted_db, input_rejected
            )
            # Apply the same relaxed comparison for user_db. In domains where
            # user_tools.db is the same object as tools.db (e.g. banking), the exact
            # hash would undo the agent_discoverable_tools relaxation above.
            if (
                gold_environment.user_tools is not None
                and gold_environment.user_tools.db is not None
            ):
                gold_user_db = gold_environment.user_tools.db.model_dump()
                predicted_user_db = predicted_environment.user_tools.db.model_dump()
                user_db_match, _ = _verified_db_match(
                    gold_user_db, predicted_user_db, input_rejected
                )
            else:
                user_db_match = (
                    gold_environment.get_user_db_hash()
                    == predicted_environment.get_user_db_hash()
                )
        else:
            agent_db_match = (
                gold_environment.get_db_hash() == predicted_environment.get_db_hash()
            )
            user_db_match = (
                gold_environment.get_user_db_hash()
                == predicted_environment.get_user_db_hash()
            )

        if agent_db_match and user_db_match:
            db_reward = 1.0
            db_match = True
        else:
            db_reward = 0.0
            db_match = False

        db_check = DBCheck(db_match=db_match, db_reward=db_reward)

        # Run env assertions
        env_assertions = task.evaluation_criteria.env_assertions or []
        env_assertion_checks = []
        env_assertion_reward = 1.0
        for env_assertion in env_assertions:
            success = predicted_environment.run_env_assertion(
                env_assertion,
                raise_assertion_error=False,
            )
            res = EnvAssertionCheck(
                env_assertion=env_assertion,
                met=success,
                reward=1.0 if success else 0.0,
            )
            env_assertion_checks.append(res)
            env_assertion_reward *= res.reward

        reward = 1.0
        reward_breakdown = {}
        if RewardType.DB in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.DB] = db_reward
            reward *= db_reward
        if RewardType.ENV_ASSERTION in task.evaluation_criteria.reward_basis:
            reward_breakdown[RewardType.ENV_ASSERTION] = env_assertion_reward
            reward *= env_assertion_reward

        return RewardInfo(
            reward=reward,
            db_check=db_check,
            env_assertions=env_assertion_checks,
            reward_basis=task.evaluation_criteria.reward_basis,
            reward_breakdown=reward_breakdown,
        )
