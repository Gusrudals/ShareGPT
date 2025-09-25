"""Reusable custom widgets for the calculator GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Sequence


ButtonSpec = tuple[str, Callable[[], None]]


class ButtonPad(ttk.Frame):
    """Grid of buttons used for the calculator keypad."""

    def __init__(
        self,
        master: tk.Misc,
        *,
        layout: Sequence[Sequence[ButtonSpec]],
        padding: int = 4,
    ) -> None:
        super().__init__(master, padding=padding)
        self._build(layout)

    def _build(self, layout: Sequence[Sequence[ButtonSpec]]) -> None:
        if not layout:
            return

        max_columns = max(len(row) for row in layout)

        for row_index, row in enumerate(layout):
            self.rowconfigure(row_index, weight=1)
            for column_index, (label, command) in enumerate(row):
                self.columnconfigure(column_index, weight=1)
                button = ttk.Button(self, text=label, command=command)
                button.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew",
                    padx=2,
                    pady=2,
                )

        for column_index in range(max_columns):
            self.columnconfigure(column_index, weight=1)
