"""Tests for the basic arithmetic helpers."""

import pytest

from calculator import basic_operations as ops


def test_add() -> None:
    assert ops.add(2, 3) == 5


def test_subtract() -> None:
    assert ops.subtract(10, 4) == 6


def test_multiply() -> None:
    assert ops.multiply(7, -2) == -14


def test_divide() -> None:
    assert ops.divide(9, 3) == 3


def test_divide_by_zero() -> None:
    with pytest.raises(ZeroDivisionError):
        ops.divide(1, 0)
