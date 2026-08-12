# QuickDeck development guide

## Project and long-term goal

QuickDeck is a local Windows desktop application built with Python and PySide6.
It is intended to become a personal digital stream deck and productivity and
automation center. A configurable global hotkey will show a compact overlay of
profile-specific buttons. Actions may eventually open programs, websites,
files, or folders; send keyboard shortcuts; run Windows or PowerShell commands;
and execute safe multi-step workflows with delays. Future goals include custom
icons and colors, drag and drop, system-tray and autostart integration, window
management, a command palette, keyboard operation, local JSON configuration,
logging, robust error handling, and Windows executable packaging.

QuickDeck needs no server, account, cloud service, database, or internet
connection for its core features. User data remains local.

Do not implement planned features before the current task requires them.

## Architecture

- Keep GUI, data models, and services separate.
- Models must not contain GUI logic.
- Services encapsulate technical behavior such as storage, actions, hotkeys,
  startup, keyboard input, and window management.
- UI classes should primarily handle presentation and user interaction.
- Do not place global business logic in widgets or create a monolithic main.py.
- Prefer a small, direct design over unnecessary abstractions or design patterns.
- Use classes only when they provide clear value and dataclasses for simple data
  models where appropriate.
- Preserve the existing architecture and avoid rewriting working code without a
  concrete need.

## Code style and safety

- Write straightforward, readable Python for a developer with foundational
  Python knowledge.
- Use descriptive English names and type hints for public functions and methods.
- Give functions one clear responsibility; avoid long functions, deep nesting,
  hidden magic numbers, and unnecessary singletons.
- Comments explain why, not obvious mechanics. More detail is appropriate for
  complicated Windows-specific behavior.
- Prefer the standard library and `pathlib`; keep external dependencies minimal.
- Handle expected failures cleanly. A bad button or missing file must never crash
  the entire application.
- Use logging instead of print for diagnostics and errors.
- Never embed machine-specific development paths.
- Never use `eval()` or `exec()`, and never treat user input as Python code.
- Use `subprocess` safely and avoid `shell=True` unless it is demonstrably needed.
- Keep functions testable.

## Workflow and tests

For every change:

1. Inspect the existing code first.
2. Respect the architecture and preserve working code.
3. Make only changes needed for the current development step.
4. Do not implement future features early.
5. Add or update focused tests where behavior changes.
6. Run relevant tests and `ruff check .` before finishing.
7. Fix clearly attributable failures independently.
8. Never delete or weaken tests merely to make checks pass.
9. Summarize changed and new files, checks performed, and manual verification
   steps at handoff.

