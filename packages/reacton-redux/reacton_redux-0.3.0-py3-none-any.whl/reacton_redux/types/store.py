from __future__ import annotations

from typing import Any, Callable, Protocol, TypeVar

from typing_extensions import TypeAlias

from .actions import Action
from .reducers import Reducer

S = TypeVar("S")

A = TypeVar("A", bound=Action[Any, Any, Any])


class Dispatch(Protocol[A]):
    def __call__(self, action: A) -> A: ...


ListenerCallback: TypeAlias = Callable[[], None]

Unsubscribe: TypeAlias = Callable[[], None]


class Store(Protocol[S, A]):  # type: ignore
    dispatch: Dispatch[A]

    def get_state(self) -> S: ...

    def subscribe(self, listener: ListenerCallback) -> Unsubscribe: ...


class StoreEnhancerStoreCreator(Protocol[S, A]):
    def __call__(self, reducer: Reducer[S, A], preloaded_state: S | None) -> Store[S, A]: ...


StoreEnhancer = Callable[[StoreEnhancerStoreCreator], StoreEnhancerStoreCreator]
