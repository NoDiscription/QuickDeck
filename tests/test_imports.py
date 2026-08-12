"""Smoke tests for the initial package structure."""


def test_important_modules_can_be_imported() -> None:
    """The application entry point and main window should import cleanly."""
    from quickdeck import main
    from quickdeck.ui.main_window import MainWindow

    assert callable(main.main)
    assert MainWindow.__name__ == "MainWindow"
