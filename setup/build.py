"""Helper script to build a standalone executable with PyInstaller."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from typing import Sequence


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC_FILE = REPO_ROOT / "setup" / "scientific_calculator.spec"


def run_pyinstaller(extra_args: Sequence[str]) -> int:
    """Invoke PyInstaller with the bundled spec file.

    Parameters
    ----------
    extra_args:
        Additional command line arguments forwarded to ``pyinstaller``.
    """

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--clean",
        "--noconfirm",
        str(SPEC_FILE),
        *extra_args,
    ]
    print("Running:", " ".join(cmd))
    try:
        completed = subprocess.run(cmd, check=False)
    except FileNotFoundError as exc:  # pragma: no cover - depends on environment
        print("PyInstaller is not available:", exc)
        return 1
    return completed.returncode


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "extra",
        nargs=argparse.REMAINDER,
        help="Additional options passed directly to PyInstaller",
    )
    args = parser.parse_args(argv)
    return run_pyinstaller(args.extra)


if __name__ == "__main__":
    raise SystemExit(main())
