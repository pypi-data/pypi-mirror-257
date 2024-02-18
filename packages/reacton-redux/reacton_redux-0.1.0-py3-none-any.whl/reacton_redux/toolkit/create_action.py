from __future__ import annotations

from typing import Any, Callable, Generic, TypeAlias, TypeVar

from typing_extensions import NotRequired, TypedDict

from ..types.actions import Action

Payload = TypeVar("Payload")

Meta = TypeVar("Meta")

Error = TypeVar("Error")


class PreparedAction(TypedDict, Generic[Payload, Meta, Error]):
    payload: NotRequired[Payload]
    meta: NotRequired[Meta]
    error: NotRequired[Error]


PrepareAction: TypeAlias = Callable[..., PreparedAction[Payload, Meta, Error]]


class ActionCreator(Generic[Payload, Meta, Error]):
    def __init__(self, type: str, prepare_action: PrepareAction[Payload, Meta, Error] | None = None):
        self.type = type
        self.prepare_action = prepare_action

    def __call__(self, *args, **kwargs) -> Action[Payload, Meta, Error]:
        if self.prepare_action is not None:
            prepared = self.prepare_action(*args, **kwargs)
            action: Action = {"type": self.type}
            if "payload" in prepared:
                action["payload"] = prepared["payload"]
            if "meta" in prepared:
                action["meta"] = prepared["meta"]
            if "error" in prepared:
                action["error"] = prepared["error"]
            return action
        # noinspection PyTypeChecker
        return {"type": self.type, "payload": args[0]}

    def __str__(self):
        return self.type

    def match(self, action: Action[Any, Any, Any]) -> bool:
        return self.type == action["type"]


create_action = ActionCreator
