import reprlib

import reacton
import reacton.ipyvuetify as rv

from .reacton import use_selector


class StateRepr(reprlib.Repr):
    def repr_bytes(self, obj, level):
        return "<bytes>"


state_repr = StateRepr()
state_repr.indent = 2  # type: ignore[attr-defined]


@reacton.component
def StoreState():
    state = use_selector(lambda s: s)

    state_str = reacton.use_memo(lambda: state_repr.repr(state), [state])

    return rv.Html(tag="pre", children=[state_str])
