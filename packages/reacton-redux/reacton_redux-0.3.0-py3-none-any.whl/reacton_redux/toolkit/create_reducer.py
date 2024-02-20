from __future__ import annotations

from functools import reduce
from typing import Any, Callable, TypeVar

from typing_extensions import Self

from ..types.actions import Action
from ..types.reducers import Reducer
from .create_action import ActionCreator
from .immer import is_draft, is_draftable, produce

S = TypeVar("S")

A = TypeVar("A", bound=Action[Any, Any, Any])

T = TypeVar("T")


def freeze_draftable(value: T) -> T:
    if is_draftable(value):
        return produce(value, lambda _: None)
    return value


def create_reducer(
    initial_state: S | Callable[[], S],
    builder_callback: Callable[[Any], None],
):
    actions_map = {}
    action_matchers: list[tuple[Callable[[Any], bool], Reducer]] = []
    default_case_reducer = None

    class ReducerBuilder:
        def add_case(self, type_or_action_creator: str | ActionCreator, reducer: Reducer[S, A]) -> Self:
            nonlocal actions_map, action_matchers, default_case_reducer

            assert not action_matchers, "`builder.add_case` should only be called before calling `builder.add_matcher`"
            assert (
                default_case_reducer is None
            ), "`builder.add_case` should only be called before calling `builder.add_default_case`"

            type_ = type_or_action_creator if isinstance(type_or_action_creator, str) else type_or_action_creator.type

            assert type_, "`builder.add_case` cannot be called with an empty action type"
            assert (
                type_ not in actions_map
            ), f"`builder.add_case` cannot be called with two reducers for the same action type '{type_}'"

            actions_map[type_] = reducer
            return self

        def add_matcher(self, matcher, reducer: Reducer[S, A]) -> Self:
            nonlocal action_matchers, default_case_reducer

            assert (
                default_case_reducer is None
            ), "`builder.add_matcher` should only be called before calling `builder.add_default_case`"

            action_matchers.append((matcher, reducer))
            return self

        def add_default_case(self, reducer: Reducer[S, A]) -> Self:
            nonlocal default_case_reducer

            assert default_case_reducer is None, "`builder.add_default_case` can only be called once"

            default_case_reducer = reducer
            return self

    builder = ReducerBuilder()
    builder_callback(builder)

    if callable(initial_state):

        def get_initial_state():
            return freeze_draftable(initial_state())

    else:
        frozen_initial_state = freeze_draftable(initial_state)

        def get_initial_state():
            return frozen_initial_state

    def created_reducer(state: S | None, action: Action) -> S:
        if state is None:
            state = get_initial_state()

        case_reducers: list[Reducer[Any, Any] | None] = [
            actions_map.get(action["type"]),
            *(reducer for matcher, reducer in action_matchers if matcher(action)),
        ]

        if all(False for case_reducer in case_reducers if case_reducer is not None):
            case_reducers = [default_case_reducer]

        def fn(previous_state, case_reducer) -> S:
            if case_reducer:
                if is_draft(previous_state):
                    """
                    If it's already a draft, we must already be inside a `createNextState` call,
                    likely because this is being wrapped in `createReducer`, `createSlice`, or nested
                    inside an existing draft. It's safe to just pass the draft to the mutator.
                    """
                    result = case_reducer(previous_state, action)
                    return result if result is not None else previous_state
                elif not is_draftable(previous_state):
                    """
                    If state is not draftable (ex: a primitive, such as 0), we want to directly
                    return the caseReducer func and not wrap it with produce.
                    """
                    result = case_reducer(previous_state, action)
                    if result is None:
                        """
                        if (previousState === null) return previousState
                        """
                        raise Exception("A case reducer on a non-draftable value must not return None")
                    return result
                else:
                    return produce(previous_state, lambda draft: case_reducer(draft, action))

            return previous_state

        return reduce(fn, case_reducers, state)

    created_reducer.get_initial_state = get_initial_state  # type: ignore[attr-defined]
    return created_reducer
