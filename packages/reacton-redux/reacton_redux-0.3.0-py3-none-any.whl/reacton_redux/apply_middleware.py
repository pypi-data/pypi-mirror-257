from types import MethodType

from .compose import compose


def apply_middleware(*middlewares):
    """
    Creates a store enhancer that applies middleware to the dispatch method
    of the Redux store. This is handy for a variety of tasks, such as expressing
    asynchronous actions in a concise manner, or logging every action payload.

    Because middleware is potentially asynchronous, this should be the first
    store enhancer in the composition chain.

    Note that each middleware will be given the `dispatch` and `get_state` functions
    as named arguments.

    Args:
        *middlewares: The middleware chain to be applied.

    Returns:
        A store enhancer applying the middleware.
    """

    def wrapper1(create_store):
        def wrapper2(reducer, preloaded_state=None):
            store = create_store(reducer, preloaded_state)

            def invalid_dispatch(*args, **kwargs):
                raise Exception(
                    "Dispatching while constructing your middleware is not allowed. "
                    "Other middleware would not be applied to this dispatch."
                )

            current_dispatch = [invalid_dispatch]

            class MiddlewareApi:
                @staticmethod
                def dispatch(*args, **kwargs):
                    return current_dispatch[0](*args, **kwargs)

                @staticmethod
                def get_state():
                    return store.get_state()

            middleware_api = MiddlewareApi()

            chain = [middleware(middleware_api) for middleware in middlewares]

            current_dispatch[0] = compose(*chain)(store.dispatch)

            store.dispatch = MethodType(lambda self, *args: current_dispatch[0](args), store)
            return store

        return wrapper2

    return wrapper1
