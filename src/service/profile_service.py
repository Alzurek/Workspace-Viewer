"""Service module for managing and executing workspace profiles."""

import subprocess
import os
from src.service.data_manager import ProfileManager


class ProfileService:
    """Service class for managing workspace profiles and their associated paths."""

    def __init__(self):
        """Initialize ProfileService with a ProfileManager instance."""
        self.profiles = ProfileManager()

    @staticmethod
    def launch_all_paths_in_profile(path_list: list):
        """Launch all paths in a profile.

        Args:
            path_list (list): List of paths to launch.
        """
        for path in path_list:
            try:
                _, file_extension = os.path.splitext(path)
                if file_extension in ('.rdp', '.bat'):
                    with subprocess.Popen(path, shell=True) as process:
                        process.wait()
                else:
                    with subprocess.Popen([path]) as process:
                        process.wait()
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")

    def get_all_profiles(self):
        """Get all profiles data.

        Returns:
            dict: Dictionary containing all profile data.
        """
        return self.profiles.data

    def get_all_profile_names(self):
        """Get names of all profiles.

        Returns:
            list: List of profile names.
        """
        return [profile_data["name"] for profile_data in self.profiles.data.values()]

    def get_paths_for_profile(self, profile_id):
        """Get all paths associated with a profile.

        Args:
            profile_id: ID of the profile.

        Returns:
            list: List of paths in the profile.
        """
        return self.profiles.data[profile_id]["paths"]

    def initialize_profile(self, profile_id, profile_name):
        """Initialize a new profile.

        Args:
            profile_id: ID for the new profile.
            profile_name: Name for the new profile.

        Returns:
            bool: False if profile name exists, True if profile was created.
        """
        if profile_name in self.get_all_profile_names():
            return False  # Profile name already exists
        return self.profiles.add_profile(profile_id, profile_name)

    def delete_profile(self, profile_id):
        """Delete a profile.

        Args:
            profile_id: ID of the profile to delete.
        """
        del self.profiles.data[profile_id]

    def create_profile(self, profile_id, profile_name):
        """Create a new profile.

        Args:
            profile_id: ID for the new profile.
            profile_name: Name for the new profile.

        Returns:
            bool: False if profile name exists, True if profile was created.
        """
        if profile_name in self.get_all_profile_names():
            return False  # Profile name already exists
        return self.profiles.add_profile(profile_id, profile_name)

    def add_path_to_profile(self, profile_id, path):
        """Add a path to an existing profile.

        Args:
            profile_id: ID of the profile.
            path: Path to add to the profile.

        Returns:
            bool: Success status of the operation.
        """
        return self.profiles.add_path_to_profile(profile_id, path)

    def change_profile_name(self, profile_id, new_name):
        """Change the name of an existing profile.

        Args:
            profile_id: ID of the profile.
            new_name: New name for the profile.

        Returns:
            bool: Success status of the operation.
        """
        return self.profiles.change_profile_name(profile_id, new_name)

    def get_profile_by_id(self, profile_id):
        """Get profile name by ID.

        Args:
            profile_id: ID of the profile.

        Returns:
            str: Name of the profile.
        """
        return self.profiles.data[profile_id]["name"]

    def remove_path_from_profile(self, profile_id, path):
        """Remove a path from a profile.

        Args:
            profile_id: ID of the profile.
            path: Path to remove from the profile.
        """
        self.profiles.remove_path_from_profile(profile_id, path)
