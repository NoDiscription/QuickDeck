"""Dialog for creating and editing one deck button."""

from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from quickdeck.models import ActionDefinition, ActionType, DeckButton

ACTION_LABELS = {
    ActionType.OPEN_APPLICATION: "Anwendung starten",
    ActionType.OPEN_WEBSITE: "Webseite öffnen",
    ActionType.OPEN_FILE: "Datei öffnen",
    ActionType.OPEN_FOLDER: "Ordner öffnen",
}
DEFAULT_BACKGROUND_COLOR = "#303642"


class ButtonEditorWindow(QDialog):
    """Collect and validate the editable values of a deck button."""

    def __init__(
        self,
        button: DeckButton | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._button = button
        self._background_color = (
            button.background_color if button and button.background_color else ""
        )
        self.setWindowTitle("Button bearbeiten" if button else "Button erstellen")
        self.setMinimumWidth(480)
        self._create_ui()
        if button is not None:
            self._fill_existing_values(button)

    def get_button(self) -> DeckButton:
        """Return a button built from the validated form values."""
        action_type = self._selected_action_type()
        action_id = (
            self._button.actions[0].id
            if self._button and self._button.actions
            else str(uuid4())
        )
        return DeckButton(
            id=self._button.id if self._button else str(uuid4()),
            name=self.name_input.text().strip(),
            icon_path=self.icon_path_input.text().strip(),
            background_color=self._background_color,
            position=self._button.position if self._button else 0,
            actions=[
                ActionDefinition(
                    id=action_id,
                    type=action_type,
                    target=self.target_input.text().strip(),
                )
            ],
        )

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_input = QLineEdit()
        form.addRow("Name:", self.name_input)

        self.action_type_combo = QComboBox()
        for action_type, label in ACTION_LABELS.items():
            self.action_type_combo.addItem(label, action_type.value)
        self.action_type_combo.currentIndexChanged.connect(self._update_browse_button)
        form.addRow("Aktionstyp:", self.action_type_combo)

        self.target_input = QLineEdit()
        self.browse_button = QPushButton("Auswählen …")
        self.browse_button.clicked.connect(self._browse_target)
        target_layout = QHBoxLayout()
        target_layout.addWidget(self.target_input)
        target_layout.addWidget(self.browse_button)
        form.addRow("Ziel:", target_layout)

        self.color_button = QPushButton()
        self.color_button.clicked.connect(self._choose_color)
        self._update_color_button()
        form.addRow("Hintergrundfarbe:", self.color_button)

        self.icon_path_input = QLineEdit()
        icon_button = QPushButton("Auswählen …")
        icon_button.clicked.connect(self._browse_icon)
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_path_input)
        icon_layout.addWidget(icon_button)
        form.addRow("Icon-Pfad (optional):", icon_layout)
        main_layout.addLayout(form)

        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #ff7777;")
        self.error_label.setWordWrap(True)
        main_layout.addWidget(self.error_label)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._validate_and_accept)
        buttons.rejected.connect(self.reject)
        main_layout.addWidget(buttons)
        self._update_browse_button()

    def _fill_existing_values(self, button: DeckButton) -> None:
        self.name_input.setText(button.name)
        self.icon_path_input.setText(button.icon_path)
        if button.actions:
            action = button.actions[0]
            index = self.action_type_combo.findData(action.type.value)
            self.action_type_combo.setCurrentIndex(index)
            self.target_input.setText(action.target)
        self._update_color_button()

    def _validate_and_accept(self) -> None:
        error_message = self._validation_error()
        self.error_label.setText(error_message or "")
        if error_message is None:
            self.accept()

    def _validation_error(self) -> str | None:
        if not self.name_input.text().strip():
            return "Bitte einen Namen eingeben."
        action_type = self._selected_action_type()
        if action_type is None:
            return "Bitte einen Aktionstyp auswählen."
        target = self.target_input.text().strip()
        if not target:
            return "Bitte ein Ziel eingeben oder auswählen."
        if action_type is ActionType.OPEN_WEBSITE:
            parsed_url = urlparse(target)
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                return "Bitte eine gültige HTTP- oder HTTPS-Adresse eingeben."
        return None

    def _browse_target(self) -> None:
        action_type = self._selected_action_type()
        if action_type is ActionType.OPEN_FOLDER:
            selected_path = QFileDialog.getExistingDirectory(self, "Ordner auswählen")
        else:
            file_filter = (
                "Anwendungen (*.exe);;Alle Dateien (*)"
                if action_type is ActionType.OPEN_APPLICATION
                else "Alle Dateien (*)"
            )
            selected_path, _ = QFileDialog.getOpenFileName(
                self,
                "Ziel auswählen",
                filter=file_filter,
            )
        if selected_path:
            self.target_input.setText(str(Path(selected_path)))

    def _browse_icon(self) -> None:
        selected_path, _ = QFileDialog.getOpenFileName(
            self,
            "Icon auswählen",
            filter="Bilder (*.png *.jpg *.jpeg *.ico *.svg);;Alle Dateien (*)",
        )
        if selected_path:
            self.icon_path_input.setText(str(Path(selected_path)))

    def _choose_color(self) -> None:
        initial_color = QColor(self._background_color or DEFAULT_BACKGROUND_COLOR)
        selected_color = QColorDialog.getColor(initial_color, self)
        if selected_color.isValid():
            self._background_color = selected_color.name()
            self._update_color_button()

    def _update_color_button(self) -> None:
        color = self._background_color or DEFAULT_BACKGROUND_COLOR
        self.color_button.setText(self._background_color or "Standard")
        self.color_button.setStyleSheet(
            f"background-color: {color}; color: white; padding: 6px;"
        )

    def _update_browse_button(self) -> None:
        is_website = self._selected_action_type() is ActionType.OPEN_WEBSITE
        self.browse_button.setEnabled(not is_website)

    def _selected_action_type(self) -> ActionType | None:
        value = self.action_type_combo.currentData()
        try:
            return ActionType(value)
        except (TypeError, ValueError):
            return None
