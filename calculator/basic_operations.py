"""Implementations for the calculator's basic arithmetic operations."""

from __future__ import annotations


def add(lhs: float, rhs: float) -> float:
    """Return the sum of ``lhs`` and ``rhs``."""

    return lhs + rhs


def subtract(lhs: float, rhs: float) -> float:
    """Return the difference ``lhs - rhs``."""

    return lhs - rhs


def multiply(lhs: float, rhs: float) -> float:
    """Return the product of ``lhs`` and ``rhs``."""

    return lhs * rhs


def divide(lhs: float, rhs: float) -> float:
    """Return the quotient ``lhs / rhs``.

    A :class:`ZeroDivisionError` is raised if ``rhs`` is zero to match the
    behaviour expected from a traditional calculator.
    """

    if rhs == 0:
        raise ZeroDivisionError("Division by zero is not defined.")

    return lhs / rhs
