from src.constants.settings import APPEARANCE_SETTING
from src.service.data_manager import SettingsManager


class SettingsService:

    def __init__(self):
        self.settings = SettingsManager()

    def update_user_app_appearance(self, new_appearance_mode):
        self.settings.update_entry(APPEARANCE_SETTING, new_appearance_mode)

    def get_user_app_appearance(self):
        return self.settings.get_entry(APPEARANCE_SETTING)
