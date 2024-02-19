from functools import reduce
from typing import Any, Callable


def compose(*funcs) -> Callable[..., Any]:
    """
    Composes single-argument functions from right to left. The rightmost
    function can take multiple arguments as it provides the signature for the
    resulting composite function.

    Args:
        *funcs: The functions to compose.

    Returns:
        A function obtained by composing the argument functions from right to left.
        For example, `compose(f, g, h)` is identical to doing `lambda *args: f(g(h(*args)))`.
    """
    if not funcs:
        return lambda *args, **kwargs: args[0] if args else None
    elif len(funcs) == 1:
        return funcs[0]

    def fn(a, b):
        return lambda *args, **kwargs: a(b(*args, **kwargs))

    return reduce(fn, funcs)
