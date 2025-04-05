"""Module for managing persistent data storage through JSON files."""

import json
import os


class BaseManager:
    """Base class for managing data persistence using JSON files.

    Provides core functionality for loading, saving, and manipulating data
    stored in JSON files within the src/data folder.
    """

    def __init__(self, file_path):
        """Initialize the manager with a specific JSON file path.

        Args:
            file_path (str): Path to the JSON file for data storage.
        """
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        """Load data from the JSON file.

        Returns:
            dict: Loaded data or empty dict if file doesn't exist.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as json_file:
                return json.load(json_file)
        return {}

    def _save_data(self):
        """Save current data to the JSON file, creating directories if needed."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json.dump(self.data, json_file, indent=2)

    def add_entry(self, key, value):
        """Add a new entry to the data store.

        Args:
            key: Unique identifier for the entry.
            value: Value to store.

        Returns:
            bool: True if entry was added, False if key already exists.
        """
        if key not in self.data:
            self.data[key] = value
            self._save_data()
            return True
        return False  # Entry with the same key already exists

    def remove_entry(self, key):
        """Remove an entry from the data store.

        Args:
            key: Key of the entry to remove.

        Returns:
            bool: True if entry was removed, False if key doesn't exist.
        """
        if key in self.data:
            del self.data[key]
            self._save_data()
            return True
        return False  # Entry with the given key doesn't exist

    def update_entry(self, key, value):
        """Update an existing entry or create if it doesn't exist.

        Args:
            key: Key of the entry to update.
            value: New value to store.

        Returns:
            bool: True if entry was updated or added.
        """
        if key in self.data:
            self.data[key] = value
            self._save_data()
            return True
        return self.add_entry(key, value)  # Entry with the given key doesn't exist

    def get_entry(self, key):
        """Retrieve an entry from the data store.

        Args:
            key: Key of the entry to retrieve.

        Returns:
            The value associated with the key, or None if not found.
        """
        return self.data.get(key, None)


class ProfileManager(BaseManager):
    """Manager for handling workspace profile data storage and operations."""

    def __init__(self, file_path="data/profiles.json"):
        """Initialize ProfileManager with default or custom file path.

        Args:
            file_path (str): Path to profiles JSON file.
        """
        super().__init__(file_path)

    def add_profile(self, profile_id, profile_name):
        """Create a new profile with empty paths list.

        Args:
            profile_id: Unique identifier for the profile.
            profile_name: Display name for the profile.

        Returns:
            bool: True if profile was created, False if ID already exists.
        """
        profile_data = {"name": profile_name, "paths": []}
        return self.add_entry(key=profile_id, value=profile_data)

    def remove_profile(self, profile_id):
        """Remove a profile and all its associated paths.

        Args:
            profile_id: ID of the profile to remove.

        Returns:
            bool: True if profile was removed, False if not found.
        """
        return self.remove_entry(key=profile_id)

    def add_path_to_profile(self, profile_id, path):
        """Add a path to an existing profile's paths list.

        Args:
            profile_id: ID of the target profile.
            path: Path to add to the profile.

        Returns:
            bool: True if path was added, False if profile not found.
        """
        if profile_id in self.data:
            self.data[profile_id]["paths"].append(path)
            self._save_data()
            return True
        return False  # Profile with the given ID doesn't exist

    def remove_path_from_profile(self, profile_id, path):
        """Remove a path from a profile's paths list.

        Args:
            profile_id: ID of the target profile.
            path: Path to remove from the profile.

        Returns:
            bool: True if path was removed, False if profile not found.
        """
        if profile_id in self.data:
            self.data[profile_id]["paths"].remove(path)
            self._save_data()
            return True
        return False  # Profile with the given ID doesn't exist

    def change_profile_name(self, profile_id, new_name):
        """Update the name of an existing profile.

        Args:
            profile_id: ID of the target profile.
            new_name: New name for the profile.

        Returns:
            bool: True if name was updated, False if profile not found.
        """
        if profile_id in self.data:
            self.data[profile_id]["name"] = new_name
            self._save_data()
            return True
        return False  # Profile with the given ID doesn't exist


class SettingsManager(BaseManager):
    """Manager for handling application settings storage and operations."""

    def __init__(self, file_path="data/settings.json"):
        """Initialize SettingsManager with default or custom file path.

        Args:
            file_path (str): Path to settings JSON file.
        """
        super().__init__(file_path)
