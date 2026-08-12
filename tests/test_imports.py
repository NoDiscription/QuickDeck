"""Smoke tests for the initial package structure."""


def test_important_modules_can_be_imported() -> None:
    """The application entry point and main window should import cleanly."""
    from quickdeck import main
    from quickdeck.services import ActionService
    from quickdeck.ui.main_window import MainWindow
    from quickdeck.widgets import DeckButtonWidget

    assert callable(main.main)
    assert MainWindow.__name__ == "MainWindow"
    assert ActionService.__name__ == "ActionService"
    assert DeckButtonWidget.__name__ == "DeckButtonWidget"
