import unittest
import json
import os

from src.data_manager import DataManager


class TestDataManager(unittest.TestCase):

    def setUp(self):
        # Create a temporary file path for testing
        self.test_file_path = "test_profiles.json"
        # Create a ProfileManager instance for testing
        self.profile_manager = DataManager(self.test_file_path)

    def tearDown(self):
        # Remove the temporary file after testing
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_add_profile(self):
        # Adding a profile should return True
        self.assertTrue(self.profile_manager.add_profile("TestProfile"))
        self.assertEqual(self.profile_manager.profiles["TestProfile"], [])

        # Adding the same profile again should return False
        self.assertFalse(self.profile_manager.add_profile("TestProfile"))

    def test_remove_profile(self):
        self.profile_manager.add_profile("TestProfile")

        # Removing a profile should return True
        self.assertTrue(self.profile_manager.remove_profile("TestProfile"))
        self.assertNotIn("TestProfile", self.profile_manager.profiles)

        # Removing a non-existent profile should return False
        self.assertFalse(self.profile_manager.remove_profile("NonExistentProfile"))

    def test_add_path_to_profile(self):
        self.profile_manager.add_profile("TestProfile")

        # Adding a path to a profile should return True
        self.assertTrue(self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe"))
        self.assertIn("C:/test/file.exe", self.profile_manager.profiles["TestProfile"])

        # Adding the same path to the same profile should return False
        self.assertFalse(self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe"))

        # Adding a path to a non-existent profile should return False
        self.assertFalse(self.profile_manager.add_path_to_profile("NonExistentProfile", "C:/test/file.exe"))

    def test_remove_path_from_profile(self):
        self.profile_manager.add_profile("TestProfile")
        self.profile_manager.add_path_to_profile("TestProfile", "C:/test/file.exe")

        # Removing a path from a profile should return True
        self.assertTrue(self.profile_manager.remove_path_from_profile("TestProfile", "C:/test/file.exe"))
        self.assertNotIn("C:/test/file.exe", self.profile_manager.profiles["TestProfile"])

        # Removing a non-existent path from a profile should return False
        self.assertFalse(self.profile_manager.remove_path_from_profile("TestProfile", "NonExistentPath"))

        # Removing a path from a non-existent profile should return False
        self.assertFalse(self.profile_manager.remove_path_from_profile("NonExistentProfile", "C:/test/file.exe"))


if __name__ == '__main__':
    unittest.main()
