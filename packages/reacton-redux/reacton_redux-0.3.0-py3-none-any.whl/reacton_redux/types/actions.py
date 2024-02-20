from typing import Generic, TypeVar

from typing_extensions import NotRequired, TypedDict

Payload = TypeVar("Payload")

Meta = TypeVar("Meta")

Error = TypeVar("Error")


# See https://github.com/redux-utilities/flux-standard-action#actions
class Action(TypedDict, Generic[Payload, Meta, Error]):
    type: str
    payload: NotRequired[Payload]
    meta: NotRequired[Meta]
    error: NotRequired[Error]
