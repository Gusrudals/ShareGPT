"""Function dispatch helpers for the calculator engine."""

from __future__ import annotations

from typing import Callable, Mapping, MutableMapping, Sequence

from calculator.basic import operations as basic_ops
from calculator.context import CalculatorContext
from calculator.exceptions import OperationNotSupportedError
from calculator.scientific import operations as sci_ops

Handler = Callable[[Sequence[float], CalculatorContext], float]


def _default_handlers() -> MutableMapping[str, Handler]:
    """Return the set of built-in function handlers."""

    def _require_exact(name: str, args: Sequence[float], expected: int) -> list[float]:
        if len(args) != expected:
            raise ValueError(f"{name} expects {expected} argument(s).")
        return list(args)

    def make_angle_function(func: Callable[[float], float], name: str) -> Handler:
        def handler(args: Sequence[float], context: CalculatorContext) -> float:
            (value,) = _require_exact(name, args, 1)
            return func(context.convert_angle(value))

        return handler

    def make_unary(func: Callable[[float], float], name: str) -> Handler:
        def handler(args: Sequence[float], _: CalculatorContext) -> float:
            (value,) = _require_exact(name, args, 1)
            return func(value)

        return handler

    def logarithm_handler(args: Sequence[float], context: CalculatorContext) -> float:
        if len(args) == 1:
            (value,) = args
            base = 10.0
        elif len(args) == 2:
            value, base = args
        else:
            raise ValueError("log expects one or two arguments.")
        return sci_ops.logarithm(value, base)

    def natural_log_handler(args: Sequence[float], context: CalculatorContext) -> float:
        (value,) = _require_exact("ln", args, 1)
        return sci_ops.logarithm(value, base=sci_ops.EULER_NUMBER)

    def power_handler(args: Sequence[float], context: CalculatorContext) -> float:
        base, exponent = _require_exact("pow", args, 2)
        return basic_ops.power(base, exponent)

    return {
        "sin": make_angle_function(lambda value: sci_ops.sine(value), "sin"),
        "cos": make_angle_function(lambda value: sci_ops.cosine(value), "cos"),
        "tan": make_angle_function(lambda value: sci_ops.tangent(value), "tan"),
        "log": logarithm_handler,
        "ln": natural_log_handler,
        "exp": make_unary(sci_ops.exponential, "exp"),
        "sqrt": make_unary(sci_ops.square_root, "sqrt"),
        "pow": power_handler,
    }


class FunctionDispatcher:
    """Dispatch named functions to their handlers."""

    def __init__(self, handlers: Mapping[str, Handler] | None = None) -> None:
        self._handlers: MutableMapping[str, Handler] = _default_handlers()
        if handlers:
            for name, handler in handlers.items():
                self.register(name, handler)

    def register(self, name: str, handler: Handler) -> None:
        """Register ``handler`` under ``name``."""

        self._handlers[name.lower()] = handler

    def unregister(self, name: str) -> None:
        """Remove the handler registered for ``name``."""

        self._handlers.pop(name.lower(), None)

    def evaluate(self, name: str, args: Sequence[float], context: CalculatorContext) -> float:
        """Evaluate the function ``name`` with ``args`` and ``context``."""

        key = name.lower()
        if key not in self._handlers:
            raise OperationNotSupportedError(f"Unsupported function '{name}'.")
        return self._handlers[key](args, context)
