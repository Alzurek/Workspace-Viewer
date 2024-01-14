import unittest
import os

from src.service.data_manager import ProfileManager
from src.service.data_manager import SettingsManager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        self.test_profiles_file_path = "data/test_profiles.json"
        self.test_settings_file_path = "data/test_settings.json"

        self.profile_manager = ProfileManager(file_path=self.test_profiles_file_path)
        self.settings_manager = SettingsManager(file_path=self.test_settings_file_path)

    def tearDown(self):
        # Remove the temporary files after testing
        if os.path.exists(self.test_profiles_file_path):
            os.remove(self.test_profiles_file_path)
        if os.path.exists(self.test_settings_file_path):
            os.remove(self.test_settings_file_path)

    def test_remove_profile(self):
        # Add a profile for testing
        self.profile_manager.add_profile("DK1L-5H38", "Profile 2")
        self.assertIn("DK1L-5H38", self.profile_manager.data)

        # Remove the profile
        self.assertTrue(self.profile_manager.remove_profile("DK1L-5H38"))
        self.assertNotIn("DK1L-5H38", self.profile_manager.data)

        # Removing a non-existent profile should return False
        self.assertFalse(self.profile_manager.remove_profile("NonExistentProfile"))

    def test_add_path_to_profile(self):
        # Add a profile for testing
        self.profile_manager.add_profile("DK1L-5H38", "Profile 2")
        self.assertIn("DK1L-5H38", self.profile_manager.data)

        # Add a path to the profile
        self.assertTrue(self.profile_manager.add_path_to_profile("DK1L-5H38", "C:/example/path"))
        self.assertIn("paths", self.profile_manager.data["DK1L-5H38"])
        self.assertIn("C:/example/path", self.profile_manager.data["DK1L-5H38"]["paths"])

    def test_remove_path_from_profile(self):
        # Add a profile for testing
        self.profile_manager.add_profile("DK1L-5H38", "Profile 2")
        self.assertIn("DK1L-5H38", self.profile_manager.data)

        # Add a path to the profile
        self.profile_manager.add_path_to_profile("DK1L-5H38", "C:/example/path")
        self.assertIn("paths", self.profile_manager.data["DK1L-5H38"])
        self.assertIn("C:/example/path", self.profile_manager.data["DK1L-5H38"]["paths"])

        # Remove the path from the profile
        self.assertTrue(self.profile_manager.remove_path_from_profile("DK1L-5H38", "C:/example/path"))
        self.assertNotIn("C:/example/path", self.profile_manager.data["DK1L-5H38"]["paths"])

    def test_change_profile_name(self):
        # Add a profile for testing
        self.profile_manager.add_profile("DK1L-5H38", "Profile 2")
        self.assertIn("DK1L-5H38", self.profile_manager.data)

        # Change the profile name
        self.assertTrue(self.profile_manager.change_profile_name("DK1L-5H38", "New Profile"))
        self.assertIn("DK1L-5H38", self.profile_manager.data)
        self.assertEqual(self.profile_manager.data["DK1L-5H38"]["name"], "New Profile")

        # Changing the name of a non-existent profile should return False
        self.assertFalse(self.profile_manager.change_profile_name("NonExistentProfile", "New Name"))

    def test_add_setting(self):
        self.assertTrue(self.settings_manager.add_entry("Setting 1", True))
        self.assertEqual(self.settings_manager.data["Setting 1"], True)

        # Adding the same setting again should return False
        self.assertFalse(self.settings_manager.add_entry("Setting 1", "value2"))
        self.assertFalse(self.settings_manager.add_entry("Setting 1", True))

    def test_remove_setting(self):
        self.assertFalse(self.settings_manager.remove_entry("Setting 1"))

        self.settings_manager.add_entry("Setting 1", "value1")
        self.assertTrue(self.settings_manager.remove_entry("Setting 1"))
        self.assertNotIn("Setting 1", self.settings_manager.data)

    def test_update_setting(self):
        # Updating a non-existent setting should create a new one
        self.assertTrue(self.settings_manager.update_entry("Setting 1", "value1"))
        self.assertIn("Setting 1", self.settings_manager.data)

        # Updating an existing setting should return True
        self.assertTrue(self.settings_manager.update_entry("Setting 1", "value2"))
        self.assertEqual(self.settings_manager.data["Setting 1"], "value2")

    def test_get_existing_entry(self):
        key = "TestKey"
        value = "TestValue"
        self.settings_manager.add_entry(key, value)

        retrieved_value = self.settings_manager.get_entry(key)
        self.assertEqual(retrieved_value, value)

    def test_get_nonexistent_entry(self):
        key = "NonexistentKey"
        retrieved_value = self.settings_manager.get_entry(key)
        self.assertIsNone(retrieved_value)


if __name__ == '__main__':
    unittest.main()
