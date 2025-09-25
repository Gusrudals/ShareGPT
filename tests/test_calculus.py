"""Tests for calculus helper functions."""

import pytest

from calculator.calculus import operations as ops


def test_differentiate_polynomial() -> None:
    assert ops.differentiate("x**3 + 2*x", "x") == "3*x**2 + 2"


def test_integrate_polynomial() -> None:
    assert ops.integrate("3*x**2", "x") == "x**3"


def test_invalid_expression() -> None:
    with pytest.raises(ValueError):
        ops.differentiate("", "x")

    with pytest.raises(ValueError):
        ops.integrate("sin(y)", "1x")
