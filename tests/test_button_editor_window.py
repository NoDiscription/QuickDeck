"""Stable form-level tests for the button editor."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialogButtonBox
from pytestqt.qtbot import QtBot

from quickdeck.models import ActionType
from quickdeck.ui.button_editor_window import ButtonEditorWindow


def click_save(editor: ButtonEditorWindow, qtbot: QtBot) -> None:
    button_box = editor.findChild(QDialogButtonBox)
    save_button = button_box.button(QDialogButtonBox.StandardButton.Save)
    qtbot.mouseClick(save_button, Qt.MouseButton.LeftButton)


def test_editor_shows_validation_errors(qtbot: QtBot) -> None:
    editor = ButtonEditorWindow()
    qtbot.addWidget(editor)

    click_save(editor, qtbot)

    assert editor.result() == 0
    assert editor.error_label.text() == "Bitte einen Namen eingeben."


def test_editor_creates_valid_website_button(qtbot: QtBot) -> None:
    editor = ButtonEditorWindow()
    qtbot.addWidget(editor)
    editor.name_input.setText("Dokumentation")
    editor.action_type_combo.setCurrentIndex(
        editor.action_type_combo.findData(ActionType.OPEN_WEBSITE.value)
    )
    editor.target_input.setText("https://example.com/docs")

    click_save(editor, qtbot)

    button = editor.get_button()
    assert editor.result() == 1
    assert button.name == "Dokumentation"
    assert button.actions[0].type is ActionType.OPEN_WEBSITE
    assert button.actions[0].target == "https://example.com/docs"


def test_website_requires_http_url(qtbot: QtBot) -> None:
    editor = ButtonEditorWindow()
    qtbot.addWidget(editor)
    editor.name_input.setText("Ungültig")
    editor.action_type_combo.setCurrentIndex(
        editor.action_type_combo.findData(ActionType.OPEN_WEBSITE.value)
    )
    editor.target_input.setText("example.com")

    click_save(editor, qtbot)

    assert editor.result() == 0
    assert "HTTP" in editor.error_label.text()
