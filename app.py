"""Entry point for the scientific calculator GUI application."""

from __future__ import annotations

import tkinter as tk

from ui.main_window import MainWindow

def main() -> None:
    """Launch the graphical calculator interface."""

    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()