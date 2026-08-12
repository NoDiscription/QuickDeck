"""Execution of actions configured for QuickDeck buttons."""

import logging
import os
import subprocess
import webbrowser
from pathlib import Path
from urllib.parse import urlparse

from quickdeck.models import ActionDefinition, ActionType

LOGGER = logging.getLogger(__name__)

ERROR_MESSAGES = {
    ActionType.OPEN_APPLICATION: "Die Anwendung konnte nicht gestartet werden.",
    ActionType.OPEN_WEBSITE: "Die Webseite konnte nicht geöffnet werden.",
    ActionType.OPEN_FILE: "Die Datei konnte nicht geöffnet werden.",
    ActionType.OPEN_FOLDER: "Der Ordner konnte nicht geöffnet werden.",
}


class ActionService:
    """Execute supported actions without exposing technical errors to the UI."""

    def execute(self, action: ActionDefinition) -> str | None:
        """Execute an action and return a user-friendly error, if one occurs."""
        try:
            if action.type is ActionType.OPEN_APPLICATION:
                self._open_application(action.target)
            elif action.type is ActionType.OPEN_WEBSITE:
                self._open_website(action.target)
            elif action.type is ActionType.OPEN_FILE:
                self._open_file(action.target)
            elif action.type is ActionType.OPEN_FOLDER:
                self._open_folder(action.target)
            else:
                raise ValueError(f"Unsupported action type: {action.type}")
        except (OSError, ValueError) as error:
            LOGGER.exception("Action %s failed: %s", action.id, error)
            return ERROR_MESSAGES.get(
                action.type,
                "Die Aktion konnte nicht ausgeführt werden.",
            )
        return None

    def _open_application(self, target: str) -> None:
        normalized_target = target.strip()
        if not normalized_target:
            raise ValueError("Application target is empty")

        target_path = Path(normalized_target)
        if (target_path.is_absolute() or target_path.parent != Path(".")) and not (
            target_path.is_file()
        ):
            raise FileNotFoundError(normalized_target)

        subprocess.Popen([normalized_target])  # noqa: S603

    def _open_website(self, target: str) -> None:
        parsed_url = urlparse(target.strip())
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("Website URL must use HTTP or HTTPS")
        if not webbrowser.open(parsed_url.geturl()):
            raise OSError("Default browser did not accept the URL")

    def _open_file(self, target: str) -> None:
        file_path = Path(target).expanduser()
        if not file_path.is_file():
            raise FileNotFoundError(file_path)
        os.startfile(file_path)  # type: ignore[attr-defined]

    def _open_folder(self, target: str) -> None:
        folder_path = Path(target).expanduser()
        if not folder_path.is_dir():
            raise FileNotFoundError(folder_path)
        os.startfile(folder_path)  # type: ignore[attr-defined]
