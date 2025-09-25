"""Core calculator engine abstractions.

The real implementation will define interfaces that coordinate between the GUI
layer and individual operation modules. During Step 3 this module will expose
classes or functions to evaluate expressions securely and consistently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


class Operation(Protocol):
    """Protocol representing a calculator operation."""

    name: str

    def evaluate(self, *operands: float) -> float:
        """Execute the operation with the provided operands."""


@dataclass
class EngineConfig:
    """Placeholder configuration container for the calculator engine."""

    angle_unit: str = "radian"
    precision: int = 8


class CalculatorEngine:
    """Skeleton for the main calculator engine."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()

    def evaluate(self, expression: str) -> float:
        """Evaluate an expression.

        A NotImplementedError is raised until the actual parsing/evaluation
        logic is implemented in a subsequent development stage.
        """

        raise NotImplementedError(
            "Expression parsing will be implemented in a later development step."
        )
