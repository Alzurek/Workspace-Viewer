import json
import os


# Import and export user settings and profiles via json files in the src/data folder
class BaseManager:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as json_file:
                return json.load(json_file)
        else:
            return {}

    def save_data(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as json_file:
            json.dump(self.data, json_file, indent=2)

    def add_entry(self, key, value):
        if key not in self.data:
            self.data[key] = value
            self.save_data()
            return True
        else:
            return False  # Entry with the same key already exists

    def remove_entry(self, key):
        if key in self.data:
            del self.data[key]
            self.save_data()
            return True
        else:
            return False  # Entry with the given key doesn't exist

    def update_entry(self, key, value):
        if key in self.data:
            self.data[key] = value
            self.save_data()
            return True
        else:
            return False  # Entry with the given key doesn't exist


class ProfileManager(BaseManager):

    def __init__(self, file_path="data/profiles.json"):
        super().__init__(file_path)

    def add_profile(self, profile_name):
        return self.add_entry(key=profile_name, value=[])

    def remove_profile(self, profile_name):
        return self.remove_entry(key=profile_name)

    def add_path_to_profile(self, profile_name, path):
        if profile_name in self.data and path not in self.data[profile_name]:
            self.data[profile_name].append(path)
            self.save_data()
            return True
        else:
            return False  # Profile with the given name doesn't exist

    def remove_path_from_profile(self, profile_name, path):
        if profile_name in self.data and path in self.data[profile_name]:
            self.data[profile_name].remove(path)
            self.save_data()
            return True
        else:
            return False  # Profile or path doesn't exist


class SettingsManager(BaseManager):

    def __init__(self, file_path="settings.json"):
        super().__init__(file_path)
