"""Execution context for the calculator engine."""

from __future__ import annotations

from dataclasses import dataclass
import math

_VALID_ANGLE_UNITS = {"radian", "degree"}


@dataclass(slots=True)
class CalculatorContext:
    """Hold runtime options for expression evaluation."""

    angle_unit: str = "radian"
    precision: int = 8

    def __post_init__(self) -> None:
        if self.angle_unit not in _VALID_ANGLE_UNITS:
            raise ValueError("angle_unit must be either 'radian' or 'degree'.")
        if self.precision <= 0:
            raise ValueError("precision must be a positive integer.")

    def convert_angle(self, value: float) -> float:
        """Convert ``value`` into radians based on the configured unit."""

        if self.angle_unit == "degree":
            return math.radians(value)
        return value

    def round(self, value: float) -> float:
        """Round ``value`` according to the configured precision."""

        return round(value, self.precision)
