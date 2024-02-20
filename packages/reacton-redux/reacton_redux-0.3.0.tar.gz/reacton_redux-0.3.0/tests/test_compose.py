import pytest

from reacton_redux import compose


@pytest.fixture
def double():
    return lambda x: x * 2


@pytest.fixture
def square():
    return lambda x: x * x


@pytest.fixture
def add():
    return lambda x, y: x + y


def test_compose_composes_from_right_to_left(double, square):
    assert compose(square)(5) == 25
    assert compose(square, double)(5) == 100
    assert compose(double, square, double)(5) == 200


def test_compose_composes_functions_from_right_to_left():
    def a(next):
        return lambda x: next(x + "a")

    def b(next):
        return lambda x: next(x + "b")

    def c(next):
        return lambda x: next(x + "c")

    def final(x):
        return x

    assert compose(a, b, c)(final)("") == "abc"
    assert compose(b, c, a)(final)("") == "bca"
    assert compose(c, a, b)(final)("") == "cab"


def test_compose_can_be_seeded_with_multiple_arguments(square, add):
    assert compose(square, add)(1, 2) == 9


def test_compose_returns_the_first_given_argument_if_given_no_functions():
    assert compose()(1, 2) == 1
    assert compose()(3) == 3
    assert compose()(None) is None


def test_compose_returns_the_first_function_if_given_only_one():
    def func():
        pass

    assert compose(func) is func
