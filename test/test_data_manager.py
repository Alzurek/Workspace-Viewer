import unittest
import os

from src.data_manager import ProfileManager
from src.data_manager import SettingsManager


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

    def test_add_profile(self):
        # Adding a profile should return True
        self.assertTrue(self.profile_manager.add_profile("TestProfile"))
        self.assertEqual(self.profile_manager.data["TestProfile"], [])

        # Adding the same profile again should return False
        self.assertFalse(self.profile_manager.add_profile("TestProfile"))

    def test_remove_profile(self):
        self.profile_manager.add_profile("TestProfile")

        # Removing a profile should return True
        self.assertTrue(self.profile_manager.remove_profile("TestProfile"))
        self.assertNotIn("TestProfile", self.profile_manager.data)

        # Removing a non-existent profile should return False
        self.assertFalse(self.profile_manager.remove_profile("NonExistentProfile"))

    def test_add_path_to_profile(self):
        self.profile_manager.add_profile("TestProfile")

        # Adding a path to a profile should return True
        self.assertTrue(self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe"))
        self.assertIn("C:/test/file.exe", self.profile_manager.data["TestProfile"])

        # Adding the same path to the same profile should return False
        self.assertFalse(self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe"))

        # Adding a path to a non-existent profile should return False
        self.assertFalse(self.profile_manager.add_path_to_profile("NonExistentProfile", "C:/test/file.exe"))

    def test_remove_path_from_profile(self):
        self.profile_manager.add_profile("TestProfile")
        self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe")

        # Removing a path from a profile should return True
        self.assertTrue(self.profile_manager.remove_path_from_profile("TestProfile", "C:/test/file.exe"))
        self.assertNotIn("C:/test/file.exe", self.profile_manager.data["TestProfile"])

        # Removing a non-existent path from a profile should return False
        self.assertFalse(self.profile_manager.remove_path_from_profile("TestProfile", "NonExistentPath"))

        # Removing a path from a non-existent profile should return False
        self.assertFalse(self.profile_manager.remove_path_from_profile("NonExistentProfile", "C:/test/file.exe"))

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
        self.assertFalse(self.settings_manager.update_entry("Setting 1", "value1"))

        self.settings_manager.add_entry("Setting 1", "value1")
        self.assertTrue(self.settings_manager.update_entry("Setting 1", "value2"))
        self.assertEqual(self.settings_manager.data["Setting 1"], "value2")


if __name__ == '__main__':
    unittest.main()
