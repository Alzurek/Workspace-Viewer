import json
import os


class BaseManager:
    """
    Import and export user specific data via json files in the src/data folder
    """

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as json_file:
                return json.load(json_file)
        else:
            return {}

    def _save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as json_file:
            json.dump(self.data, json_file, indent=2)

    def add_entry(self, key, value):
        if key not in self.data:
            self.data[key] = value
            self._save_data()
            return True
        else:
            return False  # Entry with the same key already exists

    def remove_entry(self, key):
        if key in self.data:
            del self.data[key]
            self._save_data()
            return True
        else:
            return False  # Entry with the given key doesn't exist

    def update_entry(self, key, value):
        if key in self.data:
            self.data[key] = value
            self._save_data()
            return True
        else:
            # Entry with the given key doesn't exist
            return self.add_entry(key, value)

    def get_entry(self, key):
        return self.data.get(key, None)


class ProfileManager(BaseManager):

    def __init__(self, file_path="data/profiles.json"):
        super().__init__(file_path)

    def add_profile(self, profile_id, profile_name):
        profile_data = {"name": profile_name, "paths": []}
        return self.add_entry(key=profile_id, value=profile_data)

    def remove_profile(self, profile_id):
        return self.remove_entry(key=profile_id)

    def add_path_to_profile(self, profile_id, path):
        if profile_id in self.data:
            self.data[profile_id]["paths"].append(path)
            self._save_data()
            return True
        else:
            return False  # Profile with the given ID doesn't exist

    def remove_path_from_profile(self, profile_id, path):
        if profile_id in self.data:
            self.data[profile_id]["paths"].remove(path)
            self._save_data()
            return True
        else:
            return False  # Profile with the given ID doesn't exist

    def change_profile_name(self, profile_id, new_name):
        if profile_id in self.data:
            self.data[profile_id]["name"] = new_name
            self._save_data()
            return True
        else:
            return False  # Profile with the given ID doesn't exist


class SettingsManager(BaseManager):

    def __init__(self, file_path="data/settings.json"):
        super().__init__(file_path)
