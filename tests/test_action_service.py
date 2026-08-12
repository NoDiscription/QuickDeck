"""Tests for executing configured actions without launching real applications."""

import subprocess
from pathlib import Path
from unittest.mock import Mock

import pytest

import quickdeck.services.action_service as action_service_module
from quickdeck.models import ActionDefinition, ActionType
from quickdeck.services import ActionService


def make_action(action_type: ActionType, target: str) -> ActionDefinition:
    return ActionDefinition(id="test-action", type=action_type, target=target)


def test_open_application_starts_executable(monkeypatch: pytest.MonkeyPatch) -> None:
    popen = Mock()
    monkeypatch.setattr(subprocess, "Popen", popen)

    error = ActionService().execute(
        make_action(ActionType.OPEN_APPLICATION, "notepad.exe")
    )

    assert error is None
    popen.assert_called_once_with(["notepad.exe"])


def test_missing_application_returns_friendly_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(subprocess, "Popen", Mock(side_effect=FileNotFoundError))

    error = ActionService().execute(
        make_action(ActionType.OPEN_APPLICATION, "missing.exe")
    )

    assert error == "Die Anwendung konnte nicht gestartet werden."


def test_open_website_uses_default_browser(monkeypatch: pytest.MonkeyPatch) -> None:
    browser_open = Mock(return_value=True)
    monkeypatch.setattr(action_service_module.webbrowser, "open", browser_open)

    error = ActionService().execute(
        make_action(ActionType.OPEN_WEBSITE, "https://example.com/page")
    )

    assert error is None
    browser_open.assert_called_once_with("https://example.com/page")


def test_invalid_website_returns_friendly_error() -> None:
    error = ActionService().execute(
        make_action(ActionType.OPEN_WEBSITE, "example without scheme")
    )

    assert error == "Die Webseite konnte nicht geöffnet werden."


@pytest.mark.parametrize(
    ("action_type", "is_valid_method", "error_message"),
    [
        (ActionType.OPEN_FILE, "is_file", "Die Datei konnte nicht geöffnet werden."),
        (
            ActionType.OPEN_FOLDER,
            "is_dir",
            "Der Ordner konnte nicht geöffnet werden.",
        ),
    ],
)
def test_open_path_uses_windows_default_application(
    monkeypatch: pytest.MonkeyPatch,
    action_type: ActionType,
    is_valid_method: str,
    error_message: str,
) -> None:
    monkeypatch.setattr(Path, is_valid_method, Mock(return_value=True))
    startfile = Mock()
    monkeypatch.setattr(action_service_module.os, "startfile", startfile)

    error = ActionService().execute(make_action(action_type, "C:/example"))

    assert error is None
    startfile.assert_called_once_with(Path("C:/example"))


@pytest.mark.parametrize(
    ("action_type", "error_message"),
    [
        (ActionType.OPEN_FILE, "Die Datei konnte nicht geöffnet werden."),
        (ActionType.OPEN_FOLDER, "Der Ordner konnte nicht geöffnet werden."),
    ],
)
def test_missing_path_returns_friendly_error(
    action_type: ActionType,
    error_message: str,
) -> None:
    error = ActionService().execute(make_action(action_type, "missing-path"))

    assert error == error_message
