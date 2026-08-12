"""The main QuickDeck window."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from quickdeck.models import DeckButton, QuickDeckConfig
from quickdeck.services import ActionService, DeckService
from quickdeck.ui.button_editor_window import ButtonEditorWindow
from quickdeck.widgets import DeckButtonWidget

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 450


class MainWindow(QMainWindow):
    """Display the initial QuickDeck application window."""

    def __init__(
        self,
        config: QuickDeckConfig,
        action_service: ActionService,
        deck_service: DeckService,
    ) -> None:
        super().__init__()
        self._config = config
        self._action_service = action_service
        self._deck_service = deck_service
        self.setWindowTitle("QuickDeck")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setCentralWidget(self._create_content())
        self.setStyleSheet("background-color: #17191f;")

    def _create_content(self) -> QWidget:
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(8)

        title = QLabel("QuickDeck")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "color: #f5f7fa; font-size: 36px; font-weight: 600;"
        )

        subtitle = QLabel("Your productivity deck")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #aeb5c2; font-size: 16px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(24)
        self._button_grid = QGridLayout()
        self._button_grid.setSpacing(12)
        layout.addLayout(self._button_grid)
        self._refresh_button_grid()
        return content

    def _refresh_button_grid(self) -> None:
        while self._button_grid.count():
            item = self._button_grid.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        profile = self._deck_service.get_active_profile()
        for button in sorted(profile.buttons, key=lambda item: item.position):
            row, column = divmod(button.position, self._config.settings.columns)
            widget = DeckButtonWidget(button, self._action_service)
            widget.edit_requested.connect(self._edit_button)
            widget.delete_requested.connect(self._delete_button)
            self._button_grid.addWidget(widget, row, column)

        add_position = len(profile.buttons)
        row, column = divmod(add_position, self._config.settings.columns)
        add_button = QPushButton("+")
        add_button.setObjectName("addButton")
        add_button.setMinimumSize(130, 90)
        add_button.setStyleSheet(
            "font-size: 32px; color: #aeb5c2; background-color: #252a33; "
            "border: 1px dashed #697386; border-radius: 8px;"
        )
        add_button.clicked.connect(self._create_button)
        self._button_grid.addWidget(add_button, row, column)

    def _create_button(self) -> None:
        editor = ButtonEditorWindow(parent=self)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._deck_service.add_button(editor.get_button())
            self._refresh_button_grid()

    def _edit_button(self, button_id: str) -> None:
        button = self._find_button(button_id)
        editor = ButtonEditorWindow(button, self)
        if editor.exec() == QDialog.DialogCode.Accepted:
            self._deck_service.update_button(button_id, editor.get_button())
            self._refresh_button_grid()

    def _delete_button(self, button_id: str) -> None:
        button = self._find_button(button_id)
        answer = QMessageBox.question(
            self,
            "Button löschen",
            f"Button '{button.name}' wirklich löschen?",
        )
        if answer == QMessageBox.StandardButton.Yes:
            self._deck_service.delete_button(button_id)
            self._refresh_button_grid()

    def _find_button(self, button_id: str) -> DeckButton:
        return next(
            button
            for button in self._deck_service.get_active_profile().buttons
            if button.id == button_id
        )
