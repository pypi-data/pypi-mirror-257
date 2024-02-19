from __future__ import annotations

from typing import Any, Protocol, TypeVar

from .actions import Action

S = TypeVar("S")

A = TypeVar("A", bound=Action[Any, Any, Any])


class Reducer(Protocol[S, A]):  # type: ignore[misc]
    def __call__(self, state: S | None, action: A) -> S: ...
