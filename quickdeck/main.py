"""Application entry point for QuickDeck."""

import logging
import sys

from PySide6.QtWidgets import QApplication

from quickdeck.services import StorageService
from quickdeck.ui.main_window import MainWindow


def configure_logging() -> None:
    """Configure basic application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def main() -> int:
    """Create and run the QuickDeck application."""
    configure_logging()
    StorageService().load_config()
    application = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
