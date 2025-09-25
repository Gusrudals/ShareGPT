"""Scientific calculator functions used throughout the application."""

from __future__ import annotations

import math

_SUPPORTED_ANGLE_UNITS = {"radian", "degree"}
EULER_NUMBER = math.e


def _normalize_angle(value: float, angle_unit: str) -> float:
    if angle_unit not in _SUPPORTED_ANGLE_UNITS:
        raise ValueError(f"Unsupported angle unit: {angle_unit}")

    if angle_unit == "degree":
        return math.radians(value)

    return value


def sine(value: float, *, angle_unit: str = "radian") -> float:
    """Return the sine of ``value`` using the requested ``angle_unit``."""

    return math.sin(_normalize_angle(value, angle_unit))


def cosine(value: float, *, angle_unit: str = "radian") -> float:
    """Return the cosine of ``value`` using the requested ``angle_unit``."""

    return math.cos(_normalize_angle(value, angle_unit))


def tangent(value: float, *, angle_unit: str = "radian") -> float:
    """Return the tangent of ``value`` using the requested ``angle_unit``."""

    angle = _normalize_angle(value, angle_unit)
    return math.tan(angle)


def logarithm(value: float, base: float = 10.0) -> float:
    """Return ``log_base(value)``.

    ``value`` must be positive. ``base`` must be positive and different from 1.
    A :class:`ValueError` is raised when those constraints are not met.
    """

    if value <= 0:
        raise ValueError("Logarithm is only defined for positive values.")

    if base <= 0 or base == 1:
        raise ValueError("Logarithm base must be positive and not equal to 1.")

    return math.log(value, base)


def exponential(value: float) -> float:
    """Return ``e`` raised to ``value``."""

    return math.exp(value)


def square_root(value: float) -> float:
    """Return the square root of ``value``."""

    if value < 0:
        raise ValueError("Square root is only defined for non-negative values.")
    return math.sqrt(value)
