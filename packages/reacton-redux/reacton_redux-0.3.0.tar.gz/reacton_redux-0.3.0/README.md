# Reacton Redux

A Python implementation of [Redux](https://redux.js.org/) and [Redux Toolkit](https://redux-toolkit.js.org/) with bindings for [Reacton](https://reacton.solara.dev/)/[Solara](https://solara.dev/)

[![PyPI - Version](https://img.shields.io/pypi/v/reacton-redux.svg)](https://pypi.org/project/reacton-redux/)
[![PyPI - License](https://img.shields.io/pypi/l/reacton-redux)](https://github.com/egormkn/reacton-redux/blob/main/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://github.com/PyCQA/isort)
[![Linting: ruff](https://img.shields.io/badge/linting-ruff-261230)](https://github.com/astral-sh/ruff)

## Installation

```bash
pip install "reacton-redux[devtools]"
```

# Roadmap

- [x] `create_store`
- [x] `combine_reducers`
- [x] `compose`
- [x] `apply_middleware`
- [x] `reacton.StoreProvider`
- [x] `reacton.use_store`
- [x] `reacton.use_selector`
- [x] `reacton.use_dispatch`
- [x] `toolkit.create_action`
- [x] `toolkit.create_reducer`
- [ ] `toolkit.immer`
- [ ] `toolkit.create_slice`
- [ ] Documentation
- [ ] Examples
- [ ] Tests

## Links

- [Redux](https://redux.js.org/)
  - [Fundamentals of Redux Course from Dan Abramov](https://egghead.io/courses/getting-started-with-redux)
- [Immer](https://immerjs.github.io/immer/)
  - [Introducing Immer: Immutability the easy way](https://medium.com/hackernoon/introducing-immer-immutability-the-easy-way-9d73d8f71cb3)
  - [Deep dive to immer](https://hmos.dev/en/deep-dive-to-immer)
- [Tanstack Query](https://tanstack.com/query/)
  - [Tanner Linsley – Let's Build React Query in 150 Lines of Code! (React Summit Remote Edition 2021)](https://youtu.be/9SrIirrnwk0)
  - [TkDodo's blog - Inside React Query](https://tkdodo.eu/blog/inside-react-query)
- Other Python implementations of Redux publicly available on GitHub:
  - [usrlocalben/pydux](https://github.com/usrlocalben/pydux) <kbd>⭐ 113</kbd>
  - [ebrakke/python-redux](https://github.com/ebrakke/python-redux) <kbd>⭐ 32</kbd>
  - [kasbah/aioredux](https://github.com/kasbah/aioredux) <kbd>⭐ 22</kbd>
  - [Carsten-Leue/ReduxPY](https://github.com/Carsten-Leue/ReduxPY) <kbd>⭐ 14</kbd>
  - [peterpeter5/pyredux](https://github.com/peterpeter5/pyredux) <kbd>⭐ 12</kbd>
    - [avilior/reduxpy](https://github.com/avilior/reduxpy)
  - [RookieGameDevs/revived](https://github.com/RookieGameDevs/revived) <kbd>⭐ 12</kbd>
  - [sassanh/python-redux](https://github.com/sassanh/python-redux) <kbd>⭐ 2</kbd>
  - [xdusongwei/redux-python](https://github.com/xdusongwei/redux-python) <kbd>⭐ 1</kbd>
  - [CCI-Tools/redux](https://github.com/CCI-Tools/redux)
  - [pandafeeder/redux-python](https://github.com/pandafeeder/redux-python)
  - [Jumballaya/pubsub.py](https://github.com/Jumballaya/pubsub.py)
  - [thewhitepill/rstore](https://github.com/thewhitepill/rstore)
  - [immijimmi/managedstate](https://github.com/immijimmi/managedstate)
