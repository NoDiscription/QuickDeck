"""Clickable widget representing a configured deck button."""

from PySide6.QtCore import QPoint, Qt, Signal
from PySide6.QtWidgets import QMenu, QMessageBox, QPushButton, QWidget

from quickdeck.models import DeckButton
from quickdeck.services import ActionService

DEFAULT_BUTTON_COLOR = "#303642"


class DeckButtonWidget(QPushButton):
    """Execute the configured actions when clicked."""

    edit_requested = Signal(str)
    delete_requested = Signal(str)

    def __init__(
        self,
        deck_button: DeckButton,
        action_service: ActionService,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(deck_button.name, parent)
        self._deck_button = deck_button
        self._action_service = action_service
        self.setMinimumSize(130, 90)
        color = deck_button.background_color or DEFAULT_BUTTON_COLOR
        self.setStyleSheet(
            f"QPushButton {{ background-color: {color}; color: white; "
            "border: none; border-radius: 8px; font-size: 14px; padding: 8px; }}"
            "QPushButton:hover { border: 1px solid #7d8ba3; }"
        )
        self.clicked.connect(self._execute_actions)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _execute_actions(self) -> None:
        for action in self._deck_button.actions:
            error_message = self._action_service.execute(action)
            if error_message is not None:
                QMessageBox.warning(self, "QuickDeck", error_message)
                break

    def _show_context_menu(self, position: QPoint) -> None:
        menu = QMenu(self)
        edit_action = menu.addAction("Bearbeiten")
        delete_action = menu.addAction("Löschen")
        selected_action = menu.exec(self.mapToGlobal(position))
        if selected_action is edit_action:
            self.edit_requested.emit(self._deck_button.id)
        elif selected_action is delete_action:
            self.delete_requested.emit(self._deck_button.id)
