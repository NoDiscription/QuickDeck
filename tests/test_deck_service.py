"""Tests for persisted changes to deck buttons."""

from unittest.mock import Mock

import pytest

from quickdeck.models import (
    ActionDefinition,
    ActionType,
    DeckButton,
    create_default_config,
)
from quickdeck.services import DeckService


def make_button(button_id: str, name: str) -> DeckButton:
    return DeckButton(
        id=button_id,
        name=name,
        actions=[ActionDefinition(f"{button_id}-action", ActionType.OPEN_FILE, "x")],
    )


def test_add_button_updates_model_and_saves() -> None:
    config = create_default_config()
    storage_service = Mock()
    service = DeckService(config, storage_service)
    new_button = make_button("new", "Neu")

    service.add_button(new_button)

    assert service.get_active_profile().buttons[-1] == new_button
    assert new_button.position == 2
    storage_service.save_config.assert_called_once_with(config)


def test_update_button_retains_id_and_position_and_saves() -> None:
    config = create_default_config()
    storage_service = Mock()
    service = DeckService(config, storage_service)
    original = service.get_active_profile().buttons[0]
    replacement = make_button("temporary", "Geändert")

    service.update_button(original.id, replacement)

    assert replacement.id == original.id
    assert replacement.position == original.position
    assert service.get_active_profile().buttons[0] == replacement
    storage_service.save_config.assert_called_once_with(config)


def test_delete_button_updates_positions_and_saves() -> None:
    config = create_default_config()
    storage_service = Mock()
    service = DeckService(config, storage_service)
    deleted_id = service.get_active_profile().buttons[0].id

    service.delete_button(deleted_id)

    remaining = service.get_active_profile().buttons
    assert [button.position for button in remaining] == [0]
    assert all(button.id != deleted_id for button in remaining)
    storage_service.save_config.assert_called_once_with(config)


def test_changing_unknown_button_is_rejected() -> None:
    service = DeckService(create_default_config(), Mock())

    with pytest.raises(ValueError, match="does not exist"):
        service.delete_button("unknown")
