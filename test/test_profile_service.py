"""Tests for the ProfileService class."""

import unittest
import os
import tempfile
import json
from src.service.profile_service import ProfileService
from src.service.data_manager import ProfileManager


class TestProfileService(unittest.TestCase):
    """Test suite for ProfileService functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        
        # Initialize the file with an empty JSON object
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump({}, f)
        
        # Initialize service with temporary file
        self.service = ProfileService()
        self.service.profiles = ProfileManager(file_path=self.temp_file.name)

        self.test_profile_id = "test123"
        self.test_profile_name = "Test Profile"
        self.test_path = "C:/test/path.exe"

    def tearDown(self):
        """Clean up test environment."""
        # Clear all profiles
        for profile_id in list(self.service.get_all_profiles().keys()):
            self.service.delete_profile(profile_id)

        # Remove temporary file
        os.unlink(self.temp_file.name)

        # Clean up actual profiles.json if it exists
        actual_profiles_path = os.path.join('data', 'profiles.json')
        if os.path.exists(actual_profiles_path):
            os.unlink(actual_profiles_path)

    def test_create_profile(self):
        """Test profile creation."""
        # Create a new profile
        result = self.service.create_profile(self.test_profile_id, self.test_profile_name)
        self.assertTrue(result)
        self.assertIn(self.test_profile_id, self.service.get_all_profiles())
        self.assertEqual(
            self.service.get_profile_by_id(self.test_profile_id),
            self.test_profile_name
        )

    def test_create_duplicate_profile(self):
        """Test creating a profile with duplicate name."""
        # Create initial profile
        self.service.create_profile(self.test_profile_id, self.test_profile_name)

        # Try to create another profile with same name
        result = self.service.create_profile("test456", self.test_profile_name)
        self.assertFalse(result)

    def test_add_path_to_profile(self):
        """Test adding paths to a profile."""
        # Create profile first
        self.service.create_profile(self.test_profile_id, self.test_profile_name)

        # Add path
        result = self.service.add_path_to_profile(self.test_profile_id, self.test_path)
        self.assertTrue(result)
        self.assertIn(self.test_path, self.service.get_paths_for_profile(self.test_profile_id))

    def test_remove_path_from_profile(self):
        """Test removing paths from a profile."""
        # Setup: create profile and add path
        self.service.create_profile(self.test_profile_id, self.test_profile_name)
        self.service.add_path_to_profile(self.test_profile_id, self.test_path)

        # Remove path
        self.service.remove_path_from_profile(self.test_profile_id, self.test_path)
        self.assertNotIn(self.test_path, self.service.get_paths_for_profile(self.test_profile_id))

    def test_change_profile_name(self):
        """Test changing profile name."""
        # Setup: create profile
        self.service.create_profile(self.test_profile_id, self.test_profile_name)

        # Change name
        new_name = "New Profile Name"
        result = self.service.change_profile_name(self.test_profile_id, new_name)
        self.assertTrue(result)
        self.assertEqual(
            self.service.get_profile_by_id(self.test_profile_id),
            new_name
        )

    def test_get_all_profile_names(self):
        """Test retrieving all profile names."""
        # Create multiple profiles
        profiles = {
            "id1": "Profile 1",
            "id2": "Profile 2",
            "id3": "Profile 3"
        }
        for profile_id, name in profiles.items():
            self.service.create_profile(profile_id, name)

        # Check all names are returned
        names = self.service.get_all_profile_names()
        for name in profiles.values():
            self.assertIn(name, names)

    def test_get_paths_for_profile(self):
        """Test retrieving paths for a profile."""
        # Setup: create profile and add multiple paths
        self.service.create_profile(self.test_profile_id, self.test_profile_name)
        paths = [
            "C:/path1.exe",
            "C:/path2.exe",
            "C:/path3.exe"
        ]
        for path in paths:
            self.service.add_path_to_profile(self.test_profile_id, path)

        # Check all paths are returned
        profile_paths = self.service.get_paths_for_profile(self.test_profile_id)
        for path in paths:
            self.assertIn(path, profile_paths)

    def test_delete_profile(self):
        """Test profile deletion."""
        # Setup: create profile
        self.service.create_profile(self.test_profile_id, self.test_profile_name)

        # Delete profile
        self.service.delete_profile(self.test_profile_id)
        self.assertNotIn(self.test_profile_id, self.service.get_all_profiles())

    def test_initialize_profile(self):
        """Test profile initialization."""
        # Initialize new profile
        result = self.service.initialize_profile(self.test_profile_id, self.test_profile_name)
        self.assertTrue(result)
        self.assertIn(self.test_profile_id, self.service.get_all_profiles())

        # Try to initialize with existing name
        result = self.service.initialize_profile("test456", self.test_profile_name)
        self.assertFalse(result)
 