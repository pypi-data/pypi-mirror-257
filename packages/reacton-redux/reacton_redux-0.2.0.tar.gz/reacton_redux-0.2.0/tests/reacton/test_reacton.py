from __future__ import annotations

import pytest

import reacton
import reacton.ipywidgets as rw
from reacton_redux import create_store
from reacton_redux.reacton import StoreProvider, use_selector


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


@pytest.fixture
def counter_store(counter_reducer):
    return create_store(counter_reducer)


def test_store_provider_provides_store(counter_store):
    state = None

    @reacton.component
    def Test():
        nonlocal state
        state = use_selector(lambda s: s)
        return rw.Button(description="Test")

    element = StoreProvider(store=counter_store, children=(Test(),))
    component, rc = reacton.render(element, handle_error=False)
    assert state is counter_store.get_state()
