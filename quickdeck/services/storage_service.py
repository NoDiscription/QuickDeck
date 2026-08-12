"""Local JSON storage for the QuickDeck configuration."""

import json
import logging
import os
import shutil
from datetime import UTC, datetime
from pathlib import Path

from quickdeck.models.config import (
    QuickDeckConfig,
    config_from_dict,
    config_to_dict,
    create_default_config,
)

LOGGER = logging.getLogger(__name__)
APPLICATION_DIRECTORY_NAME = "QuickDeck"
CONFIG_FILE_NAME = "config.json"


class StorageService:
    """Load and save the local QuickDeck configuration."""

    def __init__(self, config_directory: Path | None = None) -> None:
        self._config_directory = config_directory

    def get_config_path(self) -> Path:
        """Return the platform-appropriate path to config.json."""
        if self._config_directory is not None:
            return self._config_directory / CONFIG_FILE_NAME

        app_data = os.environ.get("APPDATA")
        base_directory = Path(app_data) if app_data else Path.home() / ".config"
        return base_directory / APPLICATION_DIRECTORY_NAME / CONFIG_FILE_NAME

    def load_config(self) -> QuickDeckConfig:
        """Load configuration, recovering safely from missing or invalid data."""
        config_path = self.get_config_path()
        if not config_path.is_file():
            return self._create_and_save_default_config()

        try:
            text = config_path.read_text(encoding="utf-8")
            if not text.strip():
                raise ValueError("Configuration file is empty")
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError("Configuration root must be an object")
            return config_from_dict(data)
        except (
            OSError,
            UnicodeError,
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ) as error:
            LOGGER.error("Could not load configuration: %s", error)
            self._backup_invalid_config(config_path)
            return self._create_and_save_default_config()

    def save_config(self, config: QuickDeckConfig) -> None:
        """Write a human-readable configuration file."""
        config_path = self.get_config_path()
        config_path.parent.mkdir(parents=True, exist_ok=True)
        json_text = json.dumps(config_to_dict(config), indent=2, ensure_ascii=False)
        config_path.write_text(f"{json_text}\n", encoding="utf-8")

    def _create_and_save_default_config(self) -> QuickDeckConfig:
        config = create_default_config()
        self.save_config(config)
        return config

    def _backup_invalid_config(self, config_path: Path) -> None:
        if not config_path.exists():
            return

        timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")
        backup_path = config_path.with_name(f"config.invalid-{timestamp}.json")
        try:
            shutil.copy2(config_path, backup_path)
            LOGGER.info("Invalid configuration backed up to %s", backup_path)
        except OSError as error:
            LOGGER.error("Could not back up invalid configuration: %s", error)
