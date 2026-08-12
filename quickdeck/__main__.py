"""Allow QuickDeck to be started with ``python -m quickdeck``."""

from quickdeck.main import main

if __name__ == "__main__":
    raise SystemExit(main())

