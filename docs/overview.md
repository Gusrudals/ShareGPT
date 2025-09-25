# Project Overview

## Architecture summary

The calculator is organised into three primary layers:

1. **Calculation engine (`calculator/`)** – Contains the AST-driven
   :class:`~calculator.engine.CalculatorEngine` plus helper modules for
   arithmetic, scientific functions, and polynomial calculus operations.
2. **User interface (`ui/`)** – Provides the Tkinter-based
   :class:`~ui.main_window.MainWindow` and supporting widgets that drive the
   graphical application.
3. **Application entry point (`app.py`)** – Creates the Tk root window, instals
   the main UI frame, and starts the event loop.

Automated tests in ``tests/`` exercise the calculation modules, the
documentation in ``docs/`` records the design and usage details, and
PyInstaller packaging assets live under ``setup/``.

## Key features

* Safe evaluation of arithmetic expressions with configurable precision.
* Trigonometric, logarithmic, exponential, and square-root helpers with
  validation and degree/radian support.
* Polynomial differentiation and integration utilities for a single variable.
* Desktop GUI with keypad, scientific function buttons, angle-unit selector,
  precision control, and a calculus panel.
