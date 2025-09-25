"""Core calculator engine implementation."""

from __future__ import annotations

import ast
import math

from calculator.basic import operations as basic_ops
from calculator.context import CalculatorContext
from calculator.dispatcher import FunctionDispatcher
from calculator.exceptions import InvalidExpressionError

_ALLOWED_CONSTANTS = {"pi": math.pi, "e": math.e}


class CalculatorEngine:
    """Evaluate mathematical expressions in a controlled environment."""

    def __init__(
        self,
        context: CalculatorContext | None = None,
        dispatcher: FunctionDispatcher | None = None,
    ) -> None:
        self.context = context or CalculatorContext()
        self.dispatcher = dispatcher or FunctionDispatcher()

    def evaluate(self, expression: str) -> float:
        """Evaluate ``expression`` and return the resulting float."""

        if not expression or not expression.strip():
            raise InvalidExpressionError("Expression must not be empty.")

        try:
            parsed = ast.parse(expression, mode="eval")
        except SyntaxError as exc:
            raise InvalidExpressionError(
                f"Unable to parse expression '{expression}'."
            ) from exc

        try:
            result = self._eval(parsed)
        except InvalidExpressionError:
            raise
        except ZeroDivisionError:
            raise
        except ValueError as exc:
            raise InvalidExpressionError(str(exc)) from exc

        if not math.isfinite(result):
            raise ZeroDivisionError("Expression evaluates to an undefined value.")

        return self.context.round(result)

    # ------------------------------------------------------------------
    # AST traversal helpers
    # ------------------------------------------------------------------
    def _eval(self, node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return self._eval(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return float(node.value)
            raise InvalidExpressionError("Unsupported constant type.")

        if isinstance(node, ast.Name):
            if node.id in _ALLOWED_CONSTANTS:
                return float(_ALLOWED_CONSTANTS[node.id])
            raise InvalidExpressionError(f"Unknown identifier '{node.id}'.")

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -self._eval(node.operand)

        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
            return self._eval(node.operand)

        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)

            if isinstance(node.op, ast.Add):
                return basic_ops.add(left, right)
            if isinstance(node.op, ast.Sub):
                return basic_ops.subtract(left, right)
            if isinstance(node.op, ast.Mult):
                return basic_ops.multiply(left, right)
            if isinstance(node.op, ast.Div):
                return basic_ops.divide(left, right)
            if isinstance(node.op, ast.Pow):
                return basic_ops.power(left, right)

            raise InvalidExpressionError("Unsupported binary operation.")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise InvalidExpressionError("Unsupported function call.")
            name = node.func.id
            args = [self._eval(arg) for arg in node.args]
            return self.dispatcher.evaluate(name, args, self.context)

        raise InvalidExpressionError("Unsupported expression component.")
