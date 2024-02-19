from __future__ import annotations

from typing import Any, Callable, Iterable, Optional, TypeVar, cast

import reacton

from ..create_store import Store
from ..types.store import Dispatch
from .utils import use_force_update

S = TypeVar("S")

T = TypeVar("T")

store_context = reacton.create_context(cast(Optional[Store], None))


@reacton.component
def StoreProvider(store: Store, children: Iterable[reacton.core.Element] = ()):
    store_context.provide(store)

    children_iterator = iter(children)
    child = next(children_iterator)
    if any(True for _ in children_iterator):
        raise Exception("StoreProvider should have exactly one child")

    return child


def use_store() -> Store:
    store = reacton.use_context(store_context)
    if store is None:
        raise Exception("Please provide store context with StoreProvider")
    return store


def use_selector(selector: Callable[[S], T]) -> T:
    store = cast(Store[S, Any], use_store())
    force_update = use_force_update()

    value = selector(store.get_state())

    def on_update():
        new_value = selector(store.get_state())
        if new_value is not value:
            force_update()

    reacton.use_effect(lambda: store.subscribe(on_update), [])

    return value


def use_dispatch() -> Dispatch:
    store = use_store()
    return store.dispatch
