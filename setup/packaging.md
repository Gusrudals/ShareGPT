# Packaging Guide

This document explains how to create a standalone Windows executable for the
scientific calculator using PyInstaller.

## Prerequisites

1. Install the project dependencies and PyInstaller in your virtual environment:

   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. On Windows, ensure that the version of Python you are using matches the
   target architecture (for example, 64-bit Python to produce a 64-bit
   executable).

## Building the executable

Run the helper script from the project root:

```bash
python setup/build.py
```

The script invokes PyInstaller with the bundled
`setup/scientific_calculator.spec`. On success, the packaged application will be
available under the `dist/scientific-calculator/` directory alongside a
`scientific-calculator.exe` launcher.

### Passing additional PyInstaller options

Any arguments supplied after `--` are forwarded directly to PyInstaller. For
example, to embed a custom icon:

```bash
python setup/build.py -- --icon path/to/icon.ico
```

Refer to the [PyInstaller documentation](https://pyinstaller.org/) for a full
list of available options.

## Cleaning previous builds

PyInstaller writes build artefacts to the `build/` and `dist/` directories. You
can remove them manually or run:

```bash
rm -rf build dist
```

## Troubleshooting

* **Missing PyInstaller module** – install it with `pip install pyinstaller`.
* **Antivirus false positives** – sign the executable or add it to the trusted
  applications list.
* **Incorrect GUI scaling** – adjust Windows display scaling or add a manifest
  file that specifies DPI awareness, then pass it to PyInstaller via the
  `--manifest` option.
