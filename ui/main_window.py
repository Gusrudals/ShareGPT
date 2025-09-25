"""Tkinter-based main window for the scientific calculator."""

from __future__ import annotations

import functools
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable

from calculator.calculus_operations import differentiate, integrate
from calculator.engine import CalculatorEngine, EngineConfig
from ui.widgets import ButtonPad


class MainWindow(ttk.Frame):
    """Build and manage the calculator interface."""

    def __init__(self, master: tk.Tk) -> None:
        super().__init__(master, padding=12)

        self._root = master
        self._root.title("Scientific Calculator")
        self._root.geometry("520x640")
        self._root.minsize(480, 560)
        self._root.rowconfigure(0, weight=1)
        self._root.columnconfigure(0, weight=1)

        self.grid(sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.engine = CalculatorEngine()
        self.expression_var = tk.StringVar()
        self.result_var = tk.StringVar(value="0")
        self.angle_unit_var = tk.StringVar(value=self.engine.config.angle_unit)
        self.precision_var = tk.StringVar(value=str(self.engine.config.precision))
        self.calculus_expression_var = tk.StringVar()
        self.calculus_variable_var = tk.StringVar(value="x")
        self.calculus_result_var = tk.StringVar(value="")

        self._build_calculator_panel()
        self._build_calculus_panel()

        self._root.bind("<Return>", self._handle_return)

    # ------------------------------------------------------------------
    # Layout builders
    # ------------------------------------------------------------------
    def _build_calculator_panel(self) -> None:
        calc_frame = ttk.LabelFrame(self, text="Calculator")
        calc_frame.grid(row=0, column=0, sticky="nsew")
        calc_frame.columnconfigure(0, weight=3)
        calc_frame.columnconfigure(1, weight=2)
        calc_frame.rowconfigure(1, weight=1)

        display_frame = ttk.Frame(calc_frame)
        display_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        display_frame.columnconfigure(0, weight=1)

        expression_entry = ttk.Entry(
            display_frame,
            textvariable=self.expression_var,
            font=("TkDefaultFont", 14),
        )
        expression_entry.grid(row=0, column=0, sticky="ew", padx=4, pady=(6, 2))
        expression_entry.focus_set()

        result_label = ttk.Label(
            display_frame,
            textvariable=self.result_var,
            font=("TkDefaultFont", 14),
            anchor="e",
        )
        result_label.grid(row=1, column=0, sticky="ew", padx=4, pady=(0, 8))

        options_frame = ttk.Frame(display_frame)
        options_frame.grid(row=2, column=0, sticky="ew", padx=4, pady=(0, 10))
        options_frame.columnconfigure(3, weight=1)

        ttk.Label(options_frame, text="Angle unit:").grid(row=0, column=0, sticky="w")
        angle_menu = ttk.OptionMenu(
            options_frame,
            self.angle_unit_var,
            self.angle_unit_var.get(),
            "radian",
            "degree",
            command=self._on_angle_unit_change,
        )
        angle_menu.grid(row=0, column=1, sticky="w", padx=(6, 12))

        ttk.Label(options_frame, text="Precision:").grid(row=0, column=2, sticky="w")
        precision_entry = ttk.Entry(
            options_frame,
            textvariable=self.precision_var,
            width=4,
            justify="center",
        )
        precision_entry.grid(row=0, column=3, sticky="w")

        keypad_layout = [
            [
                ("C", self.clear_expression),
                ("⌫", self.backspace),
                ("(", functools.partial(self.append_text, "(")),
                (")", functools.partial(self.append_text, ")")),
            ],
            [
                ("7", functools.partial(self.append_text, "7")),
                ("8", functools.partial(self.append_text, "8")),
                ("9", functools.partial(self.append_text, "9")),
                ("/", functools.partial(self.append_text, "/")),
            ],
            [
                ("4", functools.partial(self.append_text, "4")),
                ("5", functools.partial(self.append_text, "5")),
                ("6", functools.partial(self.append_text, "6")),
                ("*", functools.partial(self.append_text, "*")),
            ],
            [
                ("1", functools.partial(self.append_text, "1")),
                ("2", functools.partial(self.append_text, "2")),
                ("3", functools.partial(self.append_text, "3")),
                ("-", functools.partial(self.append_text, "-")),
            ],
            [
                ("0", functools.partial(self.append_text, "0")),
                (".", functools.partial(self.append_text, ".")),
                ("+", functools.partial(self.append_text, "+")),
                ("=", self.evaluate_expression),
            ],
            [
                ("^", functools.partial(self.append_text, "^")),
                ("pi", functools.partial(self.append_text, "pi")),
                ("e", functools.partial(self.append_text, "e")),
                ("Ans", self.insert_result),
            ],
        ]

        keypad = ButtonPad(calc_frame, layout=keypad_layout)
        keypad.grid(row=1, column=0, sticky="nsew", padx=(6, 4), pady=(0, 10))

        functions_frame = ttk.Frame(calc_frame)
        functions_frame.grid(row=1, column=1, sticky="nsew", padx=(4, 6), pady=(0, 10))
        functions_frame.columnconfigure(0, weight=1)

        function_buttons = [
            ("sin", functools.partial(self.append_function, "sin")),
            ("cos", functools.partial(self.append_function, "cos")),
            ("tan", functools.partial(self.append_function, "tan")),
            ("log", functools.partial(self.append_function, "log")),
            ("ln", functools.partial(self.append_function, "ln")),
            ("exp", functools.partial(self.append_function, "exp")),
            ("sqrt", functools.partial(self.append_function, "sqrt")),
        ]

        for index, (label, command) in enumerate(function_buttons):
            functions_frame.rowconfigure(index, weight=1)
            button = ttk.Button(functions_frame, text=label, command=command)
            button.grid(row=index, column=0, sticky="nsew", padx=2, pady=2)

    def _build_calculus_panel(self) -> None:
        calculus_frame = ttk.LabelFrame(self, text="Polynomial calculus")
        calculus_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))
        calculus_frame.columnconfigure(1, weight=1)
        calculus_frame.columnconfigure(2, weight=1)

        ttk.Label(calculus_frame, text="Expression:").grid(
            row=0,
            column=0,
            sticky="w",
            padx=6,
            pady=(6, 2),
        )
        expression_entry = ttk.Entry(
            calculus_frame,
            textvariable=self.calculus_expression_var,
        )
        expression_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=6, pady=(6, 2))

        ttk.Label(calculus_frame, text="Variable:").grid(
            row=1,
            column=0,
            sticky="w",
            padx=6,
            pady=(0, 6),
        )
        variable_entry = ttk.Entry(
            calculus_frame,
            textvariable=self.calculus_variable_var,
            width=6,
        )
        variable_entry.grid(row=1, column=1, sticky="w", padx=(6, 0), pady=(0, 6))

        actions_frame = ttk.Frame(calculus_frame)
        actions_frame.grid(row=1, column=2, sticky="e", padx=6, pady=(0, 6))

        differentiate_button = ttk.Button(
            actions_frame,
            text="Differentiate",
            command=self.differentiate_expression,
        )
        differentiate_button.pack(side="left", padx=(0, 6))

        integrate_button = ttk.Button(
            actions_frame,
            text="Integrate",
            command=self.integrate_expression,
        )
        integrate_button.pack(side="left")

        ttk.Label(calculus_frame, text="Result:").grid(
            row=2,
            column=0,
            sticky="nw",
            padx=6,
            pady=(0, 8),
        )
        calculus_result = ttk.Label(
            calculus_frame,
            textvariable=self.calculus_result_var,
            wraplength=360,
            justify="left",
        )
        calculus_result.grid(row=2, column=1, columnspan=2, sticky="ew", padx=6, pady=(0, 8))

    # ------------------------------------------------------------------
    # Calculator actions
    # ------------------------------------------------------------------
    def append_text(self, text: str) -> None:
        self.expression_var.set(self.expression_var.get() + text)

    def append_function(self, name: str) -> None:
        self.append_text(f"{name}(")

    def clear_expression(self) -> None:
        self.expression_var.set("")
        self.result_var.set("0")

    def insert_result(self) -> None:
        self.append_text(self.result_var.get())

    def backspace(self) -> None:
        current = self.expression_var.get()
        if current:
            self.expression_var.set(current[:-1])

    def evaluate_expression(self) -> None:
        expression = self.expression_var.get().strip()
        if not expression:
            self.result_var.set("0")
            return

        normalized_expression = expression.replace("^", "**")

        try:
            precision = int(self.precision_var.get())
        except (tk.TclError, ValueError):
            self._show_error("Precision must be a positive integer.")
            return

        if precision <= 0:
            self._show_error("Precision must be a positive integer.")
            return

        try:
            config = EngineConfig(
                angle_unit=self.angle_unit_var.get(),
                precision=precision,
            )
        except ValueError as exc:
            self._show_error(str(exc))
            return

        self.engine.config = config

        try:
            result = self.engine.evaluate(normalized_expression)
        except Exception as exc:  # pragma: no cover - GUI error feedback
            self._show_error(str(exc))
            return

        self.result_var.set(str(result))
        self.expression_var.set(str(result))

    # ------------------------------------------------------------------
    # Calculus actions
    # ------------------------------------------------------------------
    def differentiate_expression(self) -> None:
        self._run_calculus_operation(differentiate, "Differentiation error")

    def integrate_expression(self) -> None:
        self._run_calculus_operation(integrate, "Integration error")

    def _run_calculus_operation(
        self,
        operation: Callable[[str, str], str],
        title: str,
    ) -> None:
        expression = self.calculus_expression_var.get().strip()
        variable = self.calculus_variable_var.get().strip() or "x"

        if not expression:
            self._show_error("Please provide a polynomial expression to evaluate.", title=title)
            return

        try:
            result = operation(expression, variable)
        except ValueError as exc:
            self._show_error(str(exc), title=title)
            self.calculus_result_var.set("")
            return

        self.calculus_result_var.set(result)

    # ------------------------------------------------------------------
    # Event handlers and helpers
    # ------------------------------------------------------------------
    def _handle_return(self, _event: tk.Event[tk.Misc]) -> None:
        self.evaluate_expression()

    def _on_angle_unit_change(self, _value: str) -> None:
        # Validation is deferred to ``EngineConfig`` during evaluation.
        pass

    def _show_error(self, message: str, *, title: str = "Error") -> None:
        messagebox.showerror(title, message, parent=self)
