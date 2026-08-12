"""Changes to deck buttons and their persistence."""

from quickdeck.models import DeckButton, DeckProfile, QuickDeckConfig
from quickdeck.services.storage_service import StorageService


class DeckService:
    """Update the active deck profile and persist each change."""

    def __init__(
        self,
        config: QuickDeckConfig,
        storage_service: StorageService,
    ) -> None:
        self.config = config
        self._storage_service = storage_service

    def get_active_profile(self) -> DeckProfile:
        """Return the currently active profile."""
        return next(
            profile
            for profile in self.config.profiles
            if profile.id == self.config.active_profile_id
        )

    def add_button(self, button: DeckButton) -> None:
        """Append a button to the active profile and save the configuration."""
        profile = self.get_active_profile()
        button.position = len(profile.buttons)
        profile.buttons.append(button)
        self._storage_service.save_config(self.config)

    def update_button(self, button_id: str, updated_button: DeckButton) -> None:
        """Replace an existing button while retaining its identity and position."""
        profile = self.get_active_profile()
        for index, button in enumerate(profile.buttons):
            if button.id == button_id:
                updated_button.id = button.id
                updated_button.position = button.position
                profile.buttons[index] = updated_button
                self._storage_service.save_config(self.config)
                return
        raise ValueError(f"Button does not exist: {button_id}")

    def delete_button(self, button_id: str) -> None:
        """Delete a button, close position gaps, and save the configuration."""
        profile = self.get_active_profile()
        remaining_buttons = [
            button for button in profile.buttons if button.id != button_id
        ]
        if len(remaining_buttons) == len(profile.buttons):
            raise ValueError(f"Button does not exist: {button_id}")

        for position, button in enumerate(
            sorted(remaining_buttons, key=lambda item: item.position)
        ):
            button.position = position
        profile.buttons = remaining_buttons
        self._storage_service.save_config(self.config)
