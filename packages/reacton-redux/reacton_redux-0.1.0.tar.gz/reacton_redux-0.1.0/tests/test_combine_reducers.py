import pytest

from reacton_redux import combine_reducers


@pytest.fixture
def get_unique_id():
    unique_id = 0

    def next_id():
        nonlocal unique_id
        result = unique_id
        unique_id += 1
        return result

    return next_id


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
def todos_reducer(get_unique_id):
    def reducer(state: list | None, action):
        if state is None:
            return []
        elif action["type"] == "add_todo":
            payload = action["payload"]
            return [*state, {"id": get_unique_id(), "text": payload, "completed": False}]
        elif action["type"] == "remove_todo":
            payload = action["payload"]
            return [todo for todo in state if todo["id"] != payload]
        return state

    return reducer


@pytest.fixture
def combined_reducer(counter_reducer, todos_reducer):
    return combine_reducers({"counter": counter_reducer, "todos": todos_reducer})


def test_combined_reducer_is_created(combined_reducer):
    pass


def test_combined_reducer_initializes_state(combined_reducer):
    state = combined_reducer(None, {"type": "@@INIT"})
    expected_state = {"counter": 0, "todos": []}
    assert state == expected_state


def test_combined_reducer_handles_actions(combined_reducer):
    state = combined_reducer(None, {"type": "@@INIT"})
    state = combined_reducer(state, {"type": "increment"})
    state = combined_reducer(state, {"type": "add_todo", "payload": "Call mom"})
    expected_state = {
        "counter": 1,
        "todos": [{"id": 0, "text": "Call mom", "completed": False}],
    }
    assert state == expected_state
