"""Tests for the calculator engine."""

import math

import pytest

from calculator.context import CalculatorContext
from calculator.engine import CalculatorEngine
from calculator.exceptions import InvalidExpressionError, OperationNotSupportedError


def test_basic_expression_evaluation() -> None:
    engine = CalculatorEngine()
    assert engine.evaluate("2 + 3 * 4") == 14


def test_trigonometric_expression_in_radians() -> None:
    engine = CalculatorEngine()
    result = engine.evaluate("sin(pi/2)")
    assert pytest.approx(result, rel=1e-8) == 1.0


def test_trigonometric_expression_in_degrees() -> None:
    engine = CalculatorEngine(CalculatorContext(angle_unit="degree"))
    result = engine.evaluate("sin(30)")
    assert pytest.approx(result, rel=1e-8) == 0.5


def test_logarithm_with_base() -> None:
    engine = CalculatorEngine()
    result = engine.evaluate("log(100, 10)")
    assert pytest.approx(result, rel=1e-8) == 2


def test_invalid_expression_raises_invalid_expression_error() -> None:
    engine = CalculatorEngine()
    with pytest.raises(InvalidExpressionError):
        engine.evaluate("sin(x)")


def test_division_by_zero_raises() -> None:
    engine = CalculatorEngine()
    with pytest.raises(ZeroDivisionError):
        engine.evaluate("1 / 0")


def test_precision_configuration() -> None:
    engine = CalculatorEngine(CalculatorContext(precision=4))
    result = engine.evaluate("1 / 3")
    assert math.isclose(result, 0.3333, rel_tol=1e-4)


def test_unknown_function_raises_operation_not_supported() -> None:
    engine = CalculatorEngine()
    with pytest.raises(OperationNotSupportedError):
        engine.evaluate("foo(1)")
