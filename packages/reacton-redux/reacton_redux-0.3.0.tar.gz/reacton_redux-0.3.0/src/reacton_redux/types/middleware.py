from typing import Any, Callable, Protocol, TypeVar

from typing_extensions import TypeAlias

from .actions import Action
from .store import Dispatch

D = TypeVar("D", bound=Dispatch[Any])

S = TypeVar("S")


class MiddlewareApi(Protocol[D, S]):  # type: ignore[misc]
    dispatch: D

    def get_state(self) -> S: ...


MiddlewareActionHandler: TypeAlias = Callable[[Action], Any]


class Middleware(Protocol[S, D]):
    """
    A middleware is a higher-order function that composes a dispatch function
    to return a new dispatch function. It often turns async actions into
    actions.

    Middleware is composable using function composition. It is useful for
    logging actions, performing side effects like routing, or turning an
    asynchronous API call into a series of synchronous actions.
    """

    def __call__(self, api: MiddlewareApi[D, S]) -> Callable[[MiddlewareActionHandler], MiddlewareActionHandler]: ...
