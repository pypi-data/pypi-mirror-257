from __future__ import annotations

import pytest

from reacton_redux import apply_middleware, create_store


@pytest.fixture
def counter_reducer():
    def reducer(state: int | None, action):
        if state is None:
            return 0
        elif action["type"] == "increment":
            return state + 1
        elif action["type"] == "decrement":
            return state - 1
        return state

    return reducer


def test_apply_middleware_warns_when_dispatching_during_middleware_setup(counter_reducer):
    def dispatching_middleware(store):
        store.dispatch({"type": "action_dispatched_in_middleware_setup"})
        return lambda next: next

    with pytest.raises(Exception):
        apply_middleware(dispatching_middleware)(create_store)(counter_reducer)
