from typing import Any, Callable, Protocol, TypeAlias, TypeVar

from .actions import Action

A = TypeVar("A", bound=Action[Any, Any, Any])


class Dispatch(Protocol[A]):
    def __call__(self, action: A) -> A: ...


ListenerCallback: TypeAlias = Callable[[], None]
