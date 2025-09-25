# User Guide

## Launching the application

Run the following command from the project root to open the calculator window:

```
python app.py
```

The program is built with ``tkinter`` and does not require any third-party
packages.

## Calculator panel

* Enter numbers with the on-screen keypad or your keyboard.
* Use ``sin``, ``cos``, ``tan``, ``log``, ``ln``, ``exp``, and ``sqrt`` buttons to
  insert function calls – the opening parenthesis is added automatically.
* ``^`` inserts an exponent operator. Expressions typed with ``^`` are converted
  to Python's ``**`` before evaluation.
* ``Ans`` pastes the most recent result into the expression field.
* Adjust the angle unit (radians or degrees) and decimal precision using the
  controls above the keypad.
* Press ``=`` or hit the Enter key to evaluate the current expression. Results
  appear in the display below the entry field.

## Calculus panel

* Provide a polynomial expression (for example ``3*x^2 + 2*x - 5``) and the
  variable name (default: ``x``).
* Click **Differentiate** to compute the derivative or **Integrate** for the
  indefinite integral.
* Any validation errors are displayed using a pop-up dialog; correct the input
  and try again.
