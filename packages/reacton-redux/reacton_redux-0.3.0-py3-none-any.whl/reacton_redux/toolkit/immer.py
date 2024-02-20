from __future__ import annotations

from typing import Any, Callable, Generic, TypeVar

S = TypeVar("S")

P = TypeVar("P")


def is_draftable(obj: Any) -> bool:
    # return isinstance(obj, (dict, list))
    return False


class Proxy(Generic[S]):
    def __init__(self, base: S, parent: P | None = None) -> None:
        self.base = base
        self.parent = parent


create_proxy = Proxy


def is_draft(obj: Any) -> bool:
    # return isinstance(obj, Proxy)
    return False


def produce(base: S, recipe: Callable[..., S | None]) -> S:
    if is_draftable(base):
        """
        const scope = enterScope(this)
        const proxy = createProxy(base, undefined)
        let hasError = true
        try {
            result = recipe(proxy)
            hasError = false
        } finally {
            // finally instead of catch + rethrow better preserves original stack
            if (hasError) revokeScope(scope)
            else leaveScope(scope)
        }
        usePatchesInScope(scope, patchListener)
        return processResult(result, scope)
        """
        raise NotImplementedError()
    else:
        result = recipe(base)
        return result if result is not None else base
