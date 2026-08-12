"""Tests for local configuration storage."""

import json
from pathlib import Path

from quickdeck.models import (
    ActionDefinition,
    ActionType,
    DeckButton,
    create_default_config,
)
from quickdeck.services import StorageService


def test_save_config_writes_readable_json(tmp_path: Path) -> None:
    service = StorageService(tmp_path)

    service.save_config(create_default_config())

    saved_data = json.loads(service.get_config_path().read_text(encoding="utf-8"))
    assert saved_data["active_profile_id"] == "general"
    saved_text = service.get_config_path().read_text(encoding="utf-8")
    assert '\n  "config_version"' in saved_text


def test_load_config(tmp_path: Path) -> None:
    service = StorageService(tmp_path)
    config = create_default_config()
    config.settings.columns = 6
    service.save_config(config)

    loaded_config = service.load_config()

    assert loaded_config.settings.columns == 6


def test_save_and_load_roundtrip(tmp_path: Path) -> None:
    service = StorageService(tmp_path)
    config = create_default_config()
    config.profiles[0].buttons.append(
        DeckButton(
            id="browser",
            name="Website",
            icon_path="icons/browser.png",
            background_color="#334455",
            position=2,
            actions=[
                ActionDefinition(
                    id="open-site",
                    type=ActionType.OPEN_WEBSITE,
                    target="https://example.com",
                )
            ],
        )
    )

    service.save_config(config)

    assert service.load_config() == config


def test_invalid_json_is_backed_up_and_replaced(tmp_path: Path) -> None:
    service = StorageService(tmp_path)
    config_path = service.get_config_path()
    config_path.write_text("{not valid json", encoding="utf-8")

    loaded_config = service.load_config()

    assert loaded_config == create_default_config()
    assert json.loads(config_path.read_text(encoding="utf-8"))["config_version"] == 1
    backups = list(tmp_path.glob("config.invalid-*.json"))
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == "{not valid json"


def test_missing_config_is_created(tmp_path: Path) -> None:
    service = StorageService(tmp_path)

    loaded_config = service.load_config()

    assert loaded_config == create_default_config()
    assert service.get_config_path().is_file()


def test_missing_required_fields_are_recovered(tmp_path: Path) -> None:
    service = StorageService(tmp_path)
    service.get_config_path().write_text('{"config_version": 1}', encoding="utf-8")

    loaded_config = service.load_config()

    assert loaded_config == create_default_config()
    assert len(list(tmp_path.glob("config.invalid-*.json"))) == 1
