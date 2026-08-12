# QuickDeck

QuickDeck is a local Windows desktop application that will act as a personal
digital stream deck and productivity center. This first project stage contains
the maintainable foundation and a minimal PySide6 window only.

## Requirements

- Windows 10 or newer
- Python 3.12 recommended (Python 3.11 or newer is supported)

## Setup

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

If the `py` launcher is unavailable, replace `py -3.12` with the command for
your installed Python interpreter.

## Run the application

With the virtual environment activated:

```powershell
python -m quickdeck
```

Alternatively, use the installed console command:

```powershell
quickdeck
```

## Run checks

```powershell
pytest
ruff check .
```

