"""Custom exceptions for the calculator application."""

from __future__ import annotations


class CalculatorError(Exception):
    """Base class for calculator-specific exceptions."""


class InvalidExpressionError(CalculatorError):
    """Raised when the engine fails to parse or evaluate an expression."""


class OperationNotSupportedError(CalculatorError):
    """Raised when a requested operation has not been implemented."""
