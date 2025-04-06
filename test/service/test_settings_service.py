"""Tests for the SettingsService class."""

import unittest
import os
import tempfile
import json
from src.service.settings_service import SettingsService
from src.service.data_manager import SettingsManager


class TestSettingsService(unittest.TestCase):
    """Test suite for SettingsService functionality."""

    def setUp(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()

        # Initialize the file with an empty JSON object
        with open(self.temp_file.name, 'w', encoding='utf-8') as f:
            json.dump({}, f)

        # Initialize service with temporary file
        self.service = SettingsService()
        self.service.settings = SettingsManager(file_path=self.temp_file.name)

        # Test values
        self.test_appearance = "dark"
        self.test_profile = "test_profile"

    def tearDown(self):
        """Clean up test environment."""
        # Remove temporary file
        os.unlink(self.temp_file.name)

    def test_update_and_get_appearance(self):
        """Test updating and retrieving appearance setting."""
        # Update appearance
        self.service.update_user_app_appearance(self.test_appearance)

        # Verify update
        result = self.service.get_user_app_appearance()
        self.assertEqual(result, self.test_appearance)

    def test_update_and_get_current_profile(self):
        """Test updating and retrieving current profile setting."""
        # Update current profile
        self.service.update_current_user_profile(self.test_profile)

        # Verify update
        result = self.service.get_current_user_profile()
        self.assertEqual(result, self.test_profile)

    def test_default_values(self):
        """Test that settings return None when not set."""
        # Verify default values
        self.assertIsNone(self.service.get_user_app_appearance())
        self.assertIsNone(self.service.get_current_user_profile())
