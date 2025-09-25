"""Symbolic calculus helpers for polynomial expressions."""

from __future__ import annotations

import ast
from collections import defaultdict


def differentiate(expression: str, variable: str = "x") -> str:
    """Return the derivative of a polynomial expression."""

    polynomial = _parse_polynomial(expression, variable)
    derivative: dict[int, float] = {}

    for power, coefficient in polynomial.items():
        if power == 0:
            continue
        derivative[power - 1] = derivative.get(power - 1, 0.0) + coefficient * power

    return _format_polynomial(derivative, variable)


def integrate(expression: str, variable: str = "x") -> str:
    """Return the indefinite integral of a polynomial expression."""

    polynomial = _parse_polynomial(expression, variable)
    integral: dict[int, float] = {}

    for power, coefficient in polynomial.items():
        new_power = power + 1
        integral[new_power] = integral.get(new_power, 0.0) + coefficient / new_power

    return _format_polynomial(integral, variable)


def _parse_polynomial(expression: str, variable: str) -> dict[int, float]:
    if not expression.strip():
        raise ValueError("Expression must not be empty.")

    if not variable.isidentifier():
        raise ValueError("Variable name must be a valid identifier.")

    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Unable to parse expression '{expression}'.") from exc

    result = _collect_terms(parsed.body, variable)
    cleaned = {power: coeff for power, coeff in result.items() if coeff != 0}

    if not cleaned:
        return {0: 0.0}

    return cleaned


def _collect_terms(node: ast.AST, variable: str) -> dict[int, float]:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return {0: float(node.value)}

    if isinstance(node, ast.Name):
        if node.id != variable:
            raise ValueError(f"Unsupported variable '{node.id}'.")
        return {1: 1.0}

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        terms = _collect_terms(node.operand, variable)
        return {power: -coeff for power, coeff in terms.items()}

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.UAdd):
        return _collect_terms(node.operand, variable)

    if isinstance(node, ast.BinOp):
        if isinstance(node.op, (ast.Add, ast.Sub)):
            left = _collect_terms(node.left, variable)
            right = _collect_terms(node.right, variable)
            if isinstance(node.op, ast.Sub):
                right = {power: -coeff for power, coeff in right.items()}
            return _merge_terms(left, right)

        if isinstance(node.op, ast.Mult):
            left = _collect_terms(node.left, variable)
            right = _collect_terms(node.right, variable)
            if _is_constant(left):
                return {power: _get_constant(left) * coeff for power, coeff in right.items()}
            if _is_constant(right):
                return {power: _get_constant(right) * coeff for power, coeff in left.items()}
            raise ValueError("Polynomial multiplication must involve a constant factor.")

        if isinstance(node.op, ast.Pow):
            base = node.left
            exponent = node.right
            if not isinstance(base, ast.Name) or base.id != variable:
                raise ValueError("Only powers of the differentiation variable are supported.")
            if not isinstance(exponent, ast.Constant) or not isinstance(
                exponent.value, (int, float)
            ):
                raise ValueError("Polynomial exponents must be numeric constants.")
            power = int(exponent.value)
            if exponent.value != power or power < 0:
                raise ValueError("Polynomial exponents must be non-negative integers.")
            return {power: 1.0}

    raise ValueError("Unsupported expression for polynomial calculus operations.")


def _merge_terms(left: dict[int, float], right: dict[int, float]) -> dict[int, float]:
    result: dict[int, float] = defaultdict(float)
    for power, coeff in left.items():
        result[power] += coeff
    for power, coeff in right.items():
        result[power] += coeff
    return dict(result)


def _is_constant(terms: dict[int, float]) -> bool:
    return len(terms) == 1 and 0 in terms


def _get_constant(terms: dict[int, float]) -> float:
    return terms[0]


def _format_polynomial(terms: dict[int, float], variable: str) -> str:
    if not terms:
        return "0"

    parts: list[str] = []
    for power in sorted(terms.keys(), reverse=True):
        coeff = terms[power]
        if coeff == 0:
            continue

        coeff_str = _format_number(coeff)

        if power == 0:
            term = coeff_str
        elif power == 1:
            if coeff == 1:
                term = variable
            elif coeff == -1:
                term = f"-{variable}"
            else:
                term = f"{coeff_str}*{variable}"
        else:
            base = f"{variable}**{power}"
            if coeff == 1:
                term = base
            elif coeff == -1:
                term = f"-{base}"
            else:
                term = f"{coeff_str}*{base}"

        parts.append(term)

    if not parts:
        return "0"

    formatted = parts[0]
    for term in parts[1:]:
        if term.startswith("-"):
            formatted += f" - {term[1:]}"
        else:
            formatted += f" + {term}"

    return formatted


def _format_number(value: float) -> str:
    if value == int(value):
        return str(int(value))
    return str(value)
