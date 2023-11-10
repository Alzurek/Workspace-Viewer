import json
import os


# Import and export user settings and profiles via json files in the src/data folder
class DataManager:
    def __init__(self, file_path="profiles.json"):
        self.file_path = file_path
        self.profiles = self.load_profiles()

    def load_profiles(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as json_file:
                return json.load(json_file)
        else:
            return {}

    def save_profiles(self):
        with open(self.file_path, "w") as json_file:
            json.dump(self.profiles, json_file, indent=2)

    def add_profile(self, profile_name):
        if profile_name not in self.profiles:
            self.profiles[profile_name] = []
            self.save_profiles()
            return True
        else:
            return False  # Profile with the same name already exists

    def remove_profile(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]
            self.save_profiles()
            return True
        else:
            return False  # Profile with the given name doesn't exist

    def add_path_to_profile(self, profile_name, path):
        if profile_name in self.profiles and path not in self.profiles[profile_name]:
            self.profiles[profile_name].append(path)
            self.save_profiles()
            return True
        else:
            return False  # Profile with the given name doesn't exist

    def remove_path_from_profile(self, profile_name, path):
        if profile_name in self.profiles and path in self.profiles[profile_name]:
            self.profiles[profile_name].remove(path)
            self.save_profiles()
            return True
        else:
            return False  # Profile or path doesn't exist
