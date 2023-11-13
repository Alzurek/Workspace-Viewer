from src.service.data_manager import ProfileManager
import subprocess


class ProfileService:

    def __init__(self):
        self.profiles = ProfileManager()

    @staticmethod
    def launch_all_paths_in_profile(path_list: list):
        for path in path_list:
            try:
                subprocess.Popen([path])
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
        pass

    def get_all_profiles(self):
        return self.profiles.data

    def get_all_profile_names(self):
        return [profile_data["name"] for profile_data in self.profiles.data.values()]

    def get_paths_for_profile(self, profile_id):
        return self.profiles.data[profile_id]["paths"]

    def initialize_profile(self, profile_id, profile_name):
        if profile_name in self.get_all_profile_names():
            return False  # Profile name already exists
        return self.profiles.add_profile(profile_id, profile_name)

    def delete_profile(self, profile_id):
        del self.profiles.data[profile_id]

    def create_profile(self, profile_id, profile_name):
        if profile_name in self.get_all_profile_names():
            return False  # Profile name already exists
        return self.profiles.add_profile(profile_id, profile_name)

    def add_path_to_profile(self, profile_id, path):
        return self.profiles.add_path_to_profile(profile_id, path)

    def change_profile_name(self, profile_id, new_name):
        return self.profiles.change_profile_name(profile_id, new_name)

    def get_profile_by_id(self, profile_id):
        return self.profiles.data[profile_id]["name"]
