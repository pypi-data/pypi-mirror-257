import pytest

from reacton_redux import create_store


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


def test_store_is_created(counter_store):
    pass


def test_store_get_state_returns_state(counter_store):
    assert counter_store.get_state() == 0


def test_store_dispatch_modifies_state(counter_store):
    counter_store.dispatch({"type": "increment"})
    assert counter_store.get_state() == 1
    counter_store.dispatch({"type": "decrement"})
    assert counter_store.get_state() == 0


def test_store_subscribe_subscribes_to_state_updates(counter_store):
    times_called = 0

    def on_update():
        nonlocal times_called
        times_called += 1

    counter_store.subscribe(on_update)
    assert times_called == 0
    counter_store.dispatch({"type": "increment"})
    assert times_called == 1
    counter_store.dispatch({"type": "decrement"})
    assert times_called == 2
