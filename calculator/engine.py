"""Core calculator engine implementation."""

from __future__ import annotations

import ast
import math
from dataclasses import dataclass
from typing import Protocol


class Operation(Protocol):
    """Protocol representing a calculator operation."""

    name: str

    def evaluate(self, *operands: float) -> float:
        """Execute the operation with the provided operands."""


@dataclass
class EngineConfig:
    """Configuration options controlling expression evaluation."""

    angle_unit: str = "radian"
    precision: int = 8

    def __post_init__(self) -> None:
        if self.angle_unit not in {"radian", "degree"}:
            raise ValueError("angle_unit must be either 'radian' or 'degree'.")

        if self.precision <= 0:
            raise ValueError("precision must be a positive integer.")


class CalculatorEngine:
    """Evaluate mathematical expressions in a controlled environment."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()

    def _convert_angle(self, value: float) -> float:
        if self.config.angle_unit == "degree":
            return math.radians(value)
        return value

    def _eval_function(self, name: str, args: list[float]) -> float:
        if name == "sin":
            return math.sin(self._convert_angle(_require_args(name, args, 1)))
        if name == "cos":
            return math.cos(self._convert_angle(_require_args(name, args, 1)))
        if name == "tan":
            angle = self._convert_angle(_require_args(name, args, 1))
            return math.tan(angle)
        if name in {"log", "ln"}:
            if len(args) == 1:
                value = args[0]
                base = math.e if name == "ln" else 10.0
            elif len(args) == 2:
                value, base = args
            else:
                raise ValueError(f"{name} expects one or two arguments.")

            if value <= 0:
                raise ValueError("Logarithm is only defined for positive values.")
            if base <= 0 or base == 1:
                raise ValueError("Logarithm base must be positive and not equal to 1.")
            return math.log(value, base)
        if name == "exp":
            return math.exp(_require_args(name, args, 1))
        if name == "sqrt":
            value = _require_args(name, args, 1)
            if value < 0:
                raise ValueError("Square root is only defined for non-negative values.")
            return math.sqrt(value)

        raise ValueError(f"Unsupported function '{name}'.")

    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return self._eval(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise ValueError("Unsupported constant type.")

        if isinstance(node, ast.Name):
            if node.id == "pi":
                return math.pi
            if node.id == "e":
                return math.e
            raise ValueError(f"Unknown identifier '{node.id}'.")

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._eval(node.operand)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return self._eval(node.operand)

        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not defined.")
                return left / right
            if isinstance(node.op, ast.Pow):
                return math.pow(left, right)

            raise ValueError("Unsupported binary operation.")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Unsupported function call.")
            name = node.func.id
            args = [self._eval(arg) for arg in node.args]
            return self._eval_function(name, args)

        raise ValueError("Unsupported expression component.")

    def evaluate(self, expression: str) -> float:
        """Evaluate ``expression`` and return the resulting float."""

        if not expression or not expression.strip():
            raise ValueError("Expression must not be empty.")

        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise ValueError(f"Unable to parse expression '{expression}'.") from exc

        result = self._eval(parsed)

        if not math.isfinite(result):
            raise ZeroDivisionError("Expression evaluates to an undefined value.")

        # ``round`` behaves predictably for both integers and floats and gives us
        # a precision measured in decimal places, which is what users expect.
        return round(result, self.config.precision)


def _require_args(name: str, args: list[float], expected: int) -> float:
    if len(args) != expected:
        raise ValueError(f"{name} expects {expected} argument(s).")
    return args[0]
