"""The main QuickDeck window."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 450


class MainWindow(QMainWindow):
    """Display the initial QuickDeck application window."""

    def __init__(self) -> None:
        super().__init__()
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
        return content

