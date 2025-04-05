"""Service module for managing application settings."""

from src.constants.settings import APPEARANCE_SETTING, CURRENT_PROFILE
from src.service.data_manager import SettingsManager


class SettingsService:
    """Service class for managing application settings and user preferences."""

    def __init__(self):
        """Initialize SettingsService with a SettingsManager instance."""
        self.settings = SettingsManager()

    def update_user_app_appearance(self, new_appearance_mode):
        """Update the application's appearance mode setting.

        Args:
            new_appearance_mode: The new appearance mode to set.
        """
        self.settings.update_entry(APPEARANCE_SETTING, new_appearance_mode)

    def get_user_app_appearance(self):
        """Get the current application appearance mode setting.

        Returns:
            The current appearance mode setting.
        """
        return self.settings.get_entry(APPEARANCE_SETTING)

    def update_current_user_profile(self, current_profile):
        """Update the currently selected user profile.

        Args:
            current_profile: The profile to set as current.
        """
        self.settings.update_entry(CURRENT_PROFILE, current_profile)

    def get_current_user_profile(self):
        """Get the currently selected user profile.

        Returns:
            The current user profile.
        """
        return self.settings.get_entry(CURRENT_PROFILE)
