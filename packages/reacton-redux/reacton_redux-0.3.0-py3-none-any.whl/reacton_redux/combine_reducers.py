from __future__ import annotations

from typing import Any, TypeVar

from .types.actions import Action
from .types.reducers import Reducer

S = TypeVar("S")

A = TypeVar("A", bound=Action[Any, Any, Any])


def combine_reducers(reducers: dict[str, Reducer[S, A]]) -> Reducer[dict[str, S], A]:
    def combination(state: dict[str, S] | None, action: A) -> dict[str, S]:
        if state is None:
            state = {}
        has_changed = False
        next_state = {}
        for key, reducer in reducers.items():
            previous_state_for_key = state.get(key)
            next_state_for_key = reducer(previous_state_for_key, action)
            next_state[key] = next_state_for_key
            has_changed = has_changed or next_state_for_key is not previous_state_for_key
        return next_state if has_changed else state

    return combination
