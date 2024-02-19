import turbo_package as m
from slow_package.slow_functions import slow_add


def test_turbo_package():
    assert m.add(1, 2) == 3
    assert m.subtract(1, 2) == -1


def test_slow_package():
    assert slow_add(1, 2) == 3
