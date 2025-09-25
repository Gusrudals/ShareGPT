# Packaging and distribution assets

The files in this directory support building a standalone executable of the
scientific calculator.

* ``scientific_calculator.spec`` – PyInstaller specification describing how to
  bundle the GUI application without a console window.
* ``build.py`` – Convenience wrapper that runs PyInstaller with the spec file.
  Additional options can be forwarded after ``--`` when invoking the script.
* ``packaging.md`` – Step-by-step instructions for installing PyInstaller,
  running the build script, and troubleshooting common issues.
