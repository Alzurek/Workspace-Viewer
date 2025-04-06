"""GUI interface module for the Workspace Viewer application.

This module provides the main graphical user interface for managing and launching
workspace profiles. It uses customtkinter for a modern look and feel.
"""

import tkinter as tk
from tkinter import filedialog as fd
import uuid
import logging
import os
from PIL import Image
import customtkinter
from src.service.settings_service import SettingsService
from src.service.profile_service import ProfileService

WINDOW_HEIGHT = 550
WINDOW_WIDTH = 900
DEFAULT_APPEARANCE = "Dark"
DEFAULT_PROFILE = "No Profiles"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("UserInterface")

BASE_PATH = r'C:\Code\Coding\Hobby Projects\Workspace-Viewer\resource'
icon_path = os.path.join(BASE_PATH, 'icon.ico')
logo_path = os.path.join(BASE_PATH, 'logo.ico')
logo_light_path = os.path.join(BASE_PATH, 'logo_light.ico')


class UserInterface(customtkinter.CTk):
    """Main application window for the Workspace Viewer.

    This class manages the GUI interface, including profile management,
    application launching, and appearance settings.
    """

    def __init__(self):
        """Initialize the main application window and its components."""
        super().__init__()
        window_geometry = self._get_window_geometry()

        self.profiles = ProfileService()
        self.settings = SettingsService()
        self.current_profile_id = None
        self.dialog = None
        self.profile_menu = None
        self.application_list = []

        # Settings initialization
        self.current_appearance = self.settings.get_user_app_appearance()
        if self.current_appearance is None:
            self.current_appearance = DEFAULT_APPEARANCE
        self.geometry(window_geometry)

        self._set_current_profile(self.settings.get_current_user_profile())

        # Profiles initialization
        self.profile_name_list = self.profiles.get_all_profile_names()
        if len(self.profile_name_list) == 0:
            self.profile_name_list.append(DEFAULT_PROFILE)

        self.profile_name_id_mapping = {}
        for profile_id, profile_data in list(self.profiles.get_all_profiles().items()):
            self.profile_name_id_mapping[profile_data["name"]] = profile_id

        self.title("Application Launcher")
        self.wm_iconbitmap(icon_path)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._setup_ui()

    def _setup_ui(self):
        """Set up the user interface components."""
        # Create sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        # Profile Select
        self.logo_image = customtkinter.CTkImage(
            light_image=Image.open(logo_light_path),
            dark_image=Image.open(logo_path),
            size=(100, 100)
        )

        self.title_label = customtkinter.CTkLabel(
            self.sidebar,
            text="Application Launcher",
            image=self.logo_image,
            compound="top",
            font=customtkinter.CTkFont(size=20, weight="bold")
        )

        self.title_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=(20, 20)
        )

        self.create_profile_button = customtkinter.CTkButton(
            self.sidebar,
            text="Create Profile",
            command=self._create_profile
        )

        self.create_profile_button.grid(
            row=2,
            column=0,
            padx=20,
            pady=10
        )

        self.edit_profile_button = customtkinter.CTkButton(
            self.sidebar,
            text="Edit Profile",
            command=self._edit_profile
        )

        self.edit_profile_button.grid(
            row=2,
            column=0,
            padx=20,
            pady=(100, 30)
        )

        self._refresh_profile_list()
        # GUI Theme
        self.appearance_mode_label = customtkinter.CTkLabel(
            self.sidebar,
            text="Appearance Mode:",
            anchor="w"
        )

        self.appearance_mode_label.grid(
            row=5,
            column=0,
            padx=20,
            pady=(10, 0)
        )

        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(
            self.sidebar,
            values=["Light", "Dark", "System"],
            command=self._change_appearance_mode_event
        )

        self.appearance_mode_option_menu.grid(
            row=6,
            column=0,
            padx=20,
            pady=(10, 30)
        )
        # Set following based on saved data
        self.appearance_mode_option_menu.set(self.current_appearance)
        customtkinter.set_appearance_mode(self.current_appearance)

        self.launch_profile_button = customtkinter.CTkButton(
            self,
            text="Launch Profile",
            command=self._launch_profile
        )

        self.launch_profile_button.grid(
            row=0,
            column=1,
            padx=20,
            pady=20
        )

        self.choose_application_button = customtkinter.CTkButton(
            self,
            text="Choose Application",
            command=self._open_file_dialog
        )

        self.choose_application_button.grid(
            row=0,
            column=2,
            padx=20,
            pady=20
        )

        self.application_list_frame = customtkinter.CTkScrollableFrame(
            self,
            label_text="Applications to Launch"
        )

        self.application_list_frame.grid(
            row=1,
            column=1,
            columnspan=2,
            padx=20,
            pady=20,
            sticky="nsew"
        )
        self._refresh_path_list()

    def _select_profile(self, new_profile: str):
        """Select and update the current profile.

        Args:
            new_profile (str): Name of the profile to select.
        """
        try:
            new_profile_id = self.profile_name_id_mapping[new_profile]
            if new_profile_id == self.current_profile_id:
                logger.info("No need for update, same profile selected")
                return
            logger.info("Updating profile")
            self.current_profile_id = new_profile_id
            self.settings.update_current_user_profile(self.current_profile_id)
            self._refresh_path_list()
            logger.info("Successfully updated profile")
        except KeyError as e:
            logger.error("Profile not found in mapping: %s", e)

    def _change_appearance_mode_event(self, new_appearance_mode: str):
        """Handle appearance mode change event.

        Args:
            new_appearance_mode (str): New appearance mode to set.
        """
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.settings.update_user_app_appearance(new_appearance_mode)

    def _launch_profile(self):
        """Launch all applications in the current profile."""
        try:
            profile_name = self.profiles.get_profile_by_id(self.current_profile_id)
            logger.info("Launching profile %s", profile_name)
            self.profiles.launch_all_paths_in_profile(self.application_list)
            logger.info("Successfully launched profile")
        except (KeyError, FileNotFoundError) as e:
            logger.error("Error launching profile: %s", e)

    def _create_profile(self):
        """Create a new profile with user input."""
        try:
            logger.info("Creating profile")
            profile_name = self._popup_input(
                "Enter Profile Name",
                "Profile Creation",
                self.validate_new_profile_name
            )
            if profile_name is None:
                return  # Input cancelled
            if DEFAULT_PROFILE in self.profile_name_list:
                self.profile_name_list.remove(DEFAULT_PROFILE)
            self.profile_name_list.append(profile_name)
            uid = str(uuid.uuid4())
            self.profiles.create_profile(uid, profile_name)
            self.profile_name_id_mapping[profile_name] = uid
            self._set_current_profile(uid)
            self._refresh_profile_list()
            self._refresh_path_list()
            logger.info("Successfully created profile")
        except (ValueError, KeyError) as e:
            logger.error("Error creating profile: %s", e)

    def _refresh_profile_list(self):
        """Update the profile selection dropdown menu."""
        self.profile_menu = customtkinter.CTkOptionMenu(
            self.sidebar,
            dynamic_resizing=False,
            values=self.profile_name_list,
            command=self._select_profile
        )
        self.profile_menu.grid(row=2, column=0, padx=20, pady=(150, 10))
        if self.current_profile_id:
            self.profile_menu.set(self.profiles.get_profile_by_id(self.current_profile_id))

    def _refresh_path_list(self):
        """Update the list of applications in the current profile."""
        for child in self.application_list_frame.winfo_children():
            child.destroy()
        self.application_list = []
        if self.current_profile_id:
            for path in self.profiles.get_paths_for_profile(self.current_profile_id):
                self._add_to_application_list(path)

    def _set_current_profile(self, current_profile):
        """Set the current active profile.

        Args:
            current_profile: ID of the profile to set as current.
        """
        if current_profile in self.profiles.get_all_profiles():
            self.settings.update_current_user_profile(current_profile)
            self.current_profile_id = current_profile
        else:
            first_key = next(iter(self.profiles.get_all_profiles()), None)
            if first_key is None:
                first_key = ""

            self.current_profile_id = first_key
            self.settings.update_current_user_profile(first_key)

    def _open_file_dialog(self):
        """Open file dialog to select an application to add to the profile."""
        filetypes = [
            ("executable files", ".exe"),
            ("All Files", ".*")
        ]
        added_file = fd.askopenfilename(filetypes=filetypes)
        logger.info("Adding file to list")
        if self._add_to_application_list(added_file):
            logger.info("Successfully added file to list")
            self.profiles.add_path_to_profile(self.current_profile_id, added_file)

    def _add_to_application_list(self, added_file):
        """Add a file to the application list and create its UI element.

        Args:
            added_file (str): Path to the file to add.

        Returns:
            bool: True if file was added successfully, False otherwise.
        """
        try:
            if added_file in self.application_list:
                logger.warning("File already in list")
                return False
            if added_file == "":
                logger.warning("Selection canceled")
                return False
            self.application_list.append(added_file)
            label = PathRow(
                executable_path=added_file,
                delete_callback=self.delete_path,
                master=self.application_list_frame
            )
            label.grid(
                row=len(self.application_list) - 1,
                column=0,
                padx=10,
                pady=(0, 10),
                sticky="news"
            )
        except (ValueError, tk.TclError) as e:
            logger.error("Error adding application to list: %s", e)
            return False
        return True

    def delete_path(self, path):
        """Remove a path from the current profile.

        Args:
            path (str): Path to remove from the profile.
        """
        self.profiles.remove_path_from_profile(self.current_profile_id, path)
        self._refresh_path_list()

    def _edit_profile(self):
        """Edit the name of the current profile."""
        try:
            logger.info("Editing profile")
            new_name = self._popup_input(
                "Enter a New Profile Name",
                "Edit Profile",
                self.validate_new_profile_name
            )
            if new_name is None:
                return
            self._replace_value_in_profile_list(self.current_profile_id, new_name)
            self.profiles.change_profile_name(self.current_profile_id, new_name)
            self.profile_name_list = self.profiles.get_all_profile_names()
            self._refresh_profile_list()
            logger.info("Successfully edited profile")
        except (KeyError, ValueError) as e:
            logger.error("Error editing profile: %s", e)

    def _replace_value_in_profile_list(self, old_value, new_value):
        """Replace a value in the profile name list.

        Args:
            old_value: Value to replace.
            new_value: New value to insert.
        """
        for i, value in enumerate(self.profile_name_list):
            if value == old_value:
                self.profile_name_list[i] = new_value

    @staticmethod
    def _get_window_geometry():
        """Calculate window geometry for centering on screen.

        Returns:
            str: Window geometry string in format 'WIDTHxHEIGHT+X+Y'.
        """
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        window_x = (screen_width - WINDOW_WIDTH) // 2
        window_y = (screen_height - WINDOW_HEIGHT) // 2

        return f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}"

    def _popup_input(self, prompt, title, validation_func):
        """Handle popup input dialog with workaround for customtkinter issue.
        
        Note: This contains a workaround for a bug in customtkinter where
        text_color parameter is incorrectly named as button_hover_cover.
        This should be removed when customtkinter releases a fix.

        Args:
            prompt (str): Text to display in the input dialog.
            title (str): Title of the input dialog.
            validation_func (callable): Function to validate the input.

        Returns:
            str: User input if valid, None if cancelled.
        """
        text = prompt
        text_color = None
        x, y = self.winfo_pointerxy()
        _, _, position = self.geometry().partition("+")
        x_offset, y_offset = map(int, position.split("+"))
        dialog_x = max(0, x_offset + (x - x_offset) * 2)
        dialog_y = max(0, y_offset + (y - y_offset) // 1.5)
        dialog_geometry = f"300x150+{dialog_x}+{dialog_y}"
        while True:
            try:
                self.dialog = customtkinter.CTkInputDialog(
                    text=text,
                    title=title,
                    text_color=text_color
                )
            except tk.TclError as e:
                if 'color is None' in str(e) and text_color is not None:
                    logging.error("There was an error due to a typo in source code, "
                                  "there is a pull request on the git repo for this")
                else:
                    logging.error("Unknown error")

                child_list = []
                for _, child in self.children.items():
                    if isinstance(child, customtkinter.CTkInputDialog):
                        child_list.append(child)
                for child in child_list:
                    child.destroy()
                logger.info("Attempting to print without `text_color`")
                self.dialog = customtkinter.CTkInputDialog(text=text, title=title)
            self.dialog.geometry(dialog_geometry)
            self.dialog.geometry(dialog_geometry)
            value = self.dialog.get_input()
            if value is None:
                return None
            error = validation_func(value)
            if error:
                logger.warning("New profile name invalid")
                text_color = "brown3"
                text = error
            else:
                return value

    def validate_new_profile_name(self, profile_name):
        """Validate a new profile name.

        Args:
            profile_name (str): Name to validate.

        Returns:
            str: Error message if invalid, None if valid.
        """
        if profile_name in self.profile_name_list:
            return "Profile name in use, enter a new one"
        if profile_name == "":
            return "Profile names cannot be empty"
        logger.info("New profile name valid")
        return None


class PathRow(customtkinter.CTkFrame):
    """UI component for displaying a path in the application list."""

    def __init__(self, executable_path: str, delete_callback, master: any, **kwargs):
        """Initialize a path row.

        Args:
            executable_path (str): Path to the executable.
            delete_callback (callable): Function to call when delete button is pressed.
            master: Parent widget.
            **kwargs: Additional arguments to pass to CTkFrame.
        """
        super().__init__(master, **kwargs)

        split_path = executable_path.split('/')
        display_path = f"{split_path[0]}/.../{split_path[-1]}"

        delete_button = customtkinter.CTkButton(
            self,
            text="Delete",
            command=lambda: delete_callback(executable_path),
            fg_color="#D8524B",
            width=75
        )
        delete_button.grid(row=0, column=0)

        text_label = customtkinter.CTkLabel(self, text=display_path, anchor="w")
        text_label.grid(row=0, column=1, padx=15, sticky="news")

        self.grid_columnconfigure(1, weight=2)
