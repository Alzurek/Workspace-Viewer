from src.service.data_manager import ProfileManager


class ProfileService:

    def __init__(self):
        self.profiles = ProfileManager()

    def get_all_profiles(self):
        return self.profiles.data

    def get_all_profile_names(self):
        return list(self.profiles.data.keys())

    def get_paths_for_profile(self, profile_name):
        return self.profiles.data[profile_name]

    def initialize_profile(self, profile_name):
        return self.profiles.add_profile(profile_name)

    def delete_profile(self, profile_name):
        del self.profiles.data[profile_name]

    def create_profile(self, profile_name):
        return self.profiles.add_profile(profile_name)

    def add_path_to_profile(self, profile_name, path):
        return self.profiles.add_path_to_profile(profile_name, path)
