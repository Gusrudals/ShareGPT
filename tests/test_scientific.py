"""Tests for the scientific operation helpers."""

import math

import pytest

from calculator import scientific_operations as ops


def test_trigonometry_in_radians() -> None:
    assert pytest.approx(ops.sine(math.pi / 2)) == 1
    assert pytest.approx(ops.cosine(0)) == 1


def test_trigonometry_in_degrees() -> None:
    assert pytest.approx(ops.sine(30, angle_unit="degree")) == 0.5
    assert pytest.approx(ops.cosine(60, angle_unit="degree")) == 0.5


def test_unsupported_angle_unit() -> None:
    with pytest.raises(ValueError):
        ops.sine(10, angle_unit="gradian")


def test_tangent() -> None:
    assert pytest.approx(ops.tangent(math.pi / 4)) == pytest.approx(1)


def test_logarithm() -> None:
    assert pytest.approx(ops.logarithm(100, base=10)) == 2


def test_logarithm_invalid_arguments() -> None:
    with pytest.raises(ValueError):
        ops.logarithm(-1)

    with pytest.raises(ValueError):
        ops.logarithm(10, base=1)


def test_exponential() -> None:
    assert pytest.approx(ops.exponential(1)) == math.e
