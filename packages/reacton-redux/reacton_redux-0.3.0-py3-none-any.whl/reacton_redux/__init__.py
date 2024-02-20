try:
    from importlib import metadata
except ImportError:  # Python < 3.8
    import importlib_metadata as metadata  # type: ignore[no-redef]

from .apply_middleware import apply_middleware
from .combine_reducers import combine_reducers
from .compose import compose
from .create_store import create_store
from .types.actions import Action
from .types.middleware import Middleware, MiddlewareApi
from .types.reducers import Reducer
from .types.store import Dispatch, Store

__version__ = metadata.version(__package__)

__all__ = [
    "apply_middleware",
    "combine_reducers",
    "compose",
    "create_store",
    "Action",
    "Middleware",
    "MiddlewareApi",
    "Reducer",
    "Dispatch",
    "Store",
]
