from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar, cast

from .types.actions import Action
from .types.reducers import Reducer
from .types.store import ListenerCallback, Store, StoreEnhancer
from .utils.action_types import ActionTypes

S = TypeVar("S")

A = TypeVar("A", bound=Action[Any, Any, Any])


class StoreImpl(Generic[S, A]):
    def __init__(self, reducer: Reducer[S, A], preloaded_state: S | None = None) -> None:
        self.reducer = reducer
        self.state: S = cast(S, preloaded_state)
        self.listeners: set[ListenerCallback] = set()
        self.is_dispatching = False

        self.dispatch = self._dispatch

    def get_state(self) -> S:
        if self.is_dispatching:
            raise Exception("You may not call store.get_state() while the reducer is executing")
        return self.state

    def subscribe(self, listener: ListenerCallback) -> Callable[[], None]:
        if self.is_dispatching:
            raise Exception("You may not call store.subscribe() while the reducer is executing")

        self.listeners.add(listener)

        def unsubscribe():
            if self.is_dispatching:
                raise Exception("You may not unsubscribe from a store listener while the reducer is executing")

            self.listeners.discard(listener)

        return unsubscribe

    def _dispatch(self, action: A) -> A:
        if self.is_dispatching:
            raise Exception("Reducers may not dispatch actions")

        try:
            self.is_dispatching = True
            self.state = self.reducer(self.state, action)
        finally:
            self.is_dispatching = False

        for listener in self.listeners:
            listener()

        return action


def create_store(
    reducer: Reducer[S, A],
    preloaded_state: S | None = None,
    enhancer: StoreEnhancer | None = None,
):
    if not callable(reducer):
        raise ValueError(f"Expected the root reducer to be a function. Instead, received: '{type(reducer)}'")

    if enhancer is not None:
        if not callable(enhancer):
            raise ValueError(f"Expected the enhancer to be a function. Instead, received: '{type(enhancer)}'")

        return enhancer(create_store)(reducer, preloaded_state)

    store: Store[S, A] = StoreImpl(reducer, preloaded_state)

    store.dispatch({"type": ActionTypes.INIT})  # type: ignore[arg-type]
    return store
