"""Application entry point for QuickDeck."""

import logging
import sys

from PySide6.QtWidgets import QApplication

from quickdeck.services import ActionService, DeckService, StorageService
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
    storage_service = StorageService()
    config = storage_service.load_config()
    application = QApplication(sys.argv)
    deck_service = DeckService(config, storage_service)
    window = MainWindow(config, ActionService(), deck_service)
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
