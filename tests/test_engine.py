"""Tests for the calculator engine."""

import math

import pytest

from calculator.engine import CalculatorEngine, EngineConfig


def test_basic_expression_evaluation() -> None:
    engine = CalculatorEngine()
    assert engine.evaluate("2 + 3 * 4") == 14


def test_trigonometric_expression_in_radians() -> None:
    engine = CalculatorEngine()
    result = engine.evaluate("sin(pi/2)")
    assert pytest.approx(result, rel=1e-8) == 1.0


def test_trigonometric_expression_in_degrees() -> None:
    engine = CalculatorEngine(EngineConfig(angle_unit="degree"))
    result = engine.evaluate("sin(30)")
    assert pytest.approx(result, rel=1e-8) == 0.5


def test_logarithm_with_base() -> None:
    engine = CalculatorEngine()
    result = engine.evaluate("log(100, 10)")
    assert pytest.approx(result, rel=1e-8) == 2


def test_invalid_expression_raises_value_error() -> None:
    engine = CalculatorEngine()
    with pytest.raises(ValueError):
        engine.evaluate("sin(x)")


def test_division_by_zero_raises() -> None:
    engine = CalculatorEngine()
    with pytest.raises(ZeroDivisionError):
        engine.evaluate("1 / 0")


def test_precision_configuration() -> None:
    engine = CalculatorEngine(EngineConfig(precision=4))
    result = engine.evaluate("1 / 3")
    assert math.isclose(result, 0.3333, rel_tol=1e-4)
