"""Tests for QuickDeck configuration models."""

from quickdeck.models import AppSettings, create_default_config


def test_default_configuration() -> None:
    config = create_default_config()

    assert config.config_version == 1
    assert config.active_profile_id == "general"
    assert config.profiles[0].name == "Allgemein"
    assert [button.name for button in config.profiles[0].buttons] == [
        "Editor öffnen",
        "Python-Website",
    ]
    assert config.settings == AppSettings(
        hotkey="CTRL+D",
        columns=4,
        button_size="medium",
        hide_on_focus_lost=True,
        start_with_windows=False,
        theme="dark",
    )
