"""Data models and JSON conversion for the QuickDeck configuration."""

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any

CURRENT_CONFIG_VERSION = 1
DEFAULT_PROFILE_ID = "general"


class ActionType(StrEnum):
    """Actions currently supported by the configuration format."""

    OPEN_APPLICATION = "OPEN_APPLICATION"
    OPEN_WEBSITE = "OPEN_WEBSITE"
    OPEN_FILE = "OPEN_FILE"
    OPEN_FOLDER = "OPEN_FOLDER"


@dataclass(slots=True)
class ActionDefinition:
    """Describe one action performed by a deck button."""

    id: str
    type: ActionType
    target: str


@dataclass(slots=True)
class DeckButton:
    """Describe a button and its ordered actions."""

    id: str
    name: str
    icon_path: str = ""
    background_color: str = ""
    position: int = 0
    actions: list[ActionDefinition] = field(default_factory=list)


@dataclass(slots=True)
class DeckProfile:
    """Group the buttons belonging to one profile."""

    id: str
    name: str
    buttons: list[DeckButton] = field(default_factory=list)


@dataclass(slots=True)
class AppSettings:
    """Store application-wide user preferences."""

    hotkey: str = "CTRL+D"
    columns: int = 4
    button_size: str = "medium"
    hide_on_focus_lost: bool = True
    start_with_windows: bool = False
    theme: str = "dark"


@dataclass(slots=True)
class QuickDeckConfig:
    """Represent the complete persisted QuickDeck configuration."""

    config_version: int
    active_profile_id: str
    settings: AppSettings
    profiles: list[DeckProfile] = field(default_factory=list)


def create_default_config() -> QuickDeckConfig:
    """Create a fresh configuration with the default profile."""
    default_profile = DeckProfile(
        id=DEFAULT_PROFILE_ID,
        name="Allgemein",
        buttons=[
            DeckButton(
                id="example-notepad",
                name="Editor öffnen",
                position=0,
                actions=[
                    ActionDefinition(
                        id="open-notepad",
                        type=ActionType.OPEN_APPLICATION,
                        target="notepad.exe",
                    )
                ],
            ),
            DeckButton(
                id="example-python-website",
                name="Python-Website",
                position=1,
                actions=[
                    ActionDefinition(
                        id="open-python-website",
                        type=ActionType.OPEN_WEBSITE,
                        target="https://www.python.org/",
                    )
                ],
            ),
        ],
    )
    return QuickDeckConfig(
        config_version=CURRENT_CONFIG_VERSION,
        active_profile_id=default_profile.id,
        settings=AppSettings(),
        profiles=[default_profile],
    )


def config_to_dict(config: QuickDeckConfig) -> dict[str, Any]:
    """Convert a configuration into values supported by JSON."""
    return asdict(config)


def config_from_dict(data: dict[str, Any]) -> QuickDeckConfig:
    """Build and validate a configuration from decoded JSON data."""
    _require_keys(data, "config_version", "active_profile_id", "settings", "profiles")
    settings_data = _require_mapping(data["settings"], "settings")
    profiles_data = _require_list(data["profiles"], "profiles")

    settings = AppSettings(**settings_data)
    profiles = [_profile_from_dict(item) for item in profiles_data]
    if not profiles:
        raise ValueError("Configuration must contain at least one profile")

    active_profile_id = str(data["active_profile_id"])
    if active_profile_id not in {profile.id for profile in profiles}:
        raise ValueError("active_profile_id does not reference an existing profile")

    return QuickDeckConfig(
        config_version=int(data["config_version"]),
        active_profile_id=active_profile_id,
        settings=settings,
        profiles=profiles,
    )


def _profile_from_dict(value: Any) -> DeckProfile:
    data = _require_mapping(value, "profile")
    _require_keys(data, "id", "name", "buttons")
    button_values = _require_list(data["buttons"], "buttons")
    buttons = [_button_from_dict(item) for item in button_values]
    return DeckProfile(id=str(data["id"]), name=str(data["name"]), buttons=buttons)


def _button_from_dict(value: Any) -> DeckButton:
    data = _require_mapping(value, "button")
    _require_keys(
        data,
        "id",
        "name",
        "icon_path",
        "background_color",
        "position",
        "actions",
    )
    action_values = _require_list(data["actions"], "actions")
    actions = [_action_from_dict(item) for item in action_values]
    return DeckButton(
        id=str(data["id"]),
        name=str(data["name"]),
        icon_path=str(data["icon_path"]),
        background_color=str(data["background_color"]),
        position=int(data["position"]),
        actions=actions,
    )


def _action_from_dict(value: Any) -> ActionDefinition:
    data = _require_mapping(value, "action")
    _require_keys(data, "id", "type", "target")
    return ActionDefinition(
        id=str(data["id"]),
        type=ActionType(data["type"]),
        target=str(data["target"]),
    )


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{field_name} must be an object")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    return value


def _require_keys(data: dict[str, Any], *keys: str) -> None:
    missing_keys = [key for key in keys if key not in data]
    if missing_keys:
        raise ValueError(f"Missing required fields: {', '.join(missing_keys)}")
