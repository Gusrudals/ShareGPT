# Scientific Calculator Project

This repository hosts a Python-based scientific calculator that now includes
working arithmetic, scientific, polynomial calculus, and desktop GUI
functionality. The implementation uses Python's standard-library ``tkinter``
toolkit so the application can run without additional dependencies while still
providing an intuitive interface for everyday use.

## Current Structure
- `app.py` – Entry point for the Tkinter GUI application.
- `calculator/` – Package containing the calculation engine and operation
  modules.
- `ui/` – Package providing the Tkinter main window and reusable widgets.
- `tests/` – Automated regression tests covering the current functionality.
- `docs/` – Documentation placeholders.
- `setup/` – Future distribution/build scripts.
- `requirements.txt` – Python dependencies for upcoming implementation phases.

## Available Features

- **Basic arithmetic**: addition, subtraction, multiplication, and division
  helpers with input validation.
- **Scientific functions**: trigonometry with configurable angle units,
  exponential, and logarithmic operations.
- **Polynomial calculus**: analytic differentiation and integration for
  single-variable polynomials.
- **Expression engine**: safe AST-based evaluator that supports arithmetic,
  scientific functions, configurable precision, and angle units.
- **Desktop GUI**: Tkinter interface with keypad, scientific function buttons,
  configurable angle units, precision control, and built-in calculus helpers.

Further packaging work remains for subsequent steps of the plan.

## Running the calculator

```
python app.py
```

Launching the application opens the calculator window. Enter expressions using
the keypad or your keyboard, press ``=`` to evaluate, and use the calculus
panel at the bottom to differentiate or integrate polynomial expressions.
