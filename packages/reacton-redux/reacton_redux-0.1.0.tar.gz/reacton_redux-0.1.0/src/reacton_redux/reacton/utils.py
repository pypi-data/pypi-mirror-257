from typing import Callable

import reacton


def use_force_update() -> Callable[[], None]:
    _, set_state = reacton.use_state(0)

    def updater():
        set_state(lambda value: value + 1)

    return updater
