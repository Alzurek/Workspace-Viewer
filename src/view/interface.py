import customtkinter
import tkinter as tk
from tkinter import filedialog as fd
from src.service.settings_service import SettingsService
from src.service.profile_service import ProfileService
from PIL import Image
import uuid

WINDOW_HEIGHT = 550
WINDOW_WIDTH = 900
DEFAULT_APPEARANCE = "Dark"
DEFAULT_PROFILE = "No Profiles"


class Interface(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        window_geometry = self._get_window_geometry()

        # Settings initialization
        self.settings = SettingsService()
        self.current_appearance = self.settings.get_user_app_appearance()
        if self.current_appearance is None:
            self.current_appearance = DEFAULT_APPEARANCE
        self.geometry(window_geometry)

        self._set_current_profile(self.settings.get_current_user_profile())

        # Profiles initialization
        self.profiles = ProfileService()
        self.profile_name_list = self.profiles.get_all_profile_names()
        if len(self.profile_name_list) == 0:
            self.profile_name_list.append(DEFAULT_PROFILE)

        self.profile_name_id_mapping = {}
        for profile_id, profile_data in list(self.profiles.get_all_profiles().items()):
            self.profile_name_id_mapping[profile_data["name"]] = profile_id

        self.title("Application Launcher")
        self.wm_iconbitmap('../resource/icon.ico')
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)

        # Profile Select
        self.logo_image = customtkinter.CTkImage(light_image=Image.open("../resource/logo_light.ico"),
                                                 dark_image=Image.open("../resource/logo.ico"), size=(100, 100))

        self.title_label = customtkinter.CTkLabel(self.sidebar, text="Application Launcher", image=self.logo_image,
                                                  compound="top", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=20, pady=(20, 20))

        self.create_profile_button = customtkinter.CTkButton(self.sidebar, text="Create Profile",
                                                             command=self._create_profile)
        self.create_profile_button.grid(row=2, column=0, padx=20, pady=10)

        self.edit_profile_button = customtkinter.CTkButton(self.sidebar, text="Edit Profile", command=self._edit_profile)
        self.edit_profile_button.grid(row=2, column=0, padx=20, pady=(100, 30))

        self._refresh_profile_list()
        # GUI Theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                                       command=self._change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 30))
        # Set following based on saved data
        self.appearance_mode_option_menu.set(self.current_appearance)
        customtkinter.set_appearance_mode(self.current_appearance)

        self.launch_profile_button = customtkinter.CTkButton(self, text="Launch Profile", command=self._launch_profile)
        self.launch_profile_button.grid(row=0, column=1, padx=20, pady=20)

        self.choose_application_button = customtkinter.CTkButton(self, text="Choose Application",
                                                                 command=self._open_file_dialog)
        self.choose_application_button.grid(row=0, column=2, padx=20, pady=20)

        self.application_list_frame = customtkinter.CTkScrollableFrame(self, label_text="Applications to Launch")
        self.application_list_frame.grid(row=1, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self._refresh_path_list()

    def _select_profile(self, new_profile: str):
        self.current_profile_id = self.profile_name_id_mapping[new_profile]
        self.settings.update_current_user_profile(self.current_profile_id)
        self._refresh_path_list()
        print("Updated profile")

    def _change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.settings.update_user_app_appearance(new_appearance_mode)

    def _launch_profile(self):
        # TODO launch profile
        print(f"Launching profile {self.profiles.get_profile_by_id(self.current_profile_id)}")

    def _create_profile(self):
        print(f"create profile")
        profile_name = self._popup_input("Enter Profile Name", "Profile Creation", self.validate_new_profile_name)
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

    def _refresh_profile_list(self):
        self.profile_menu = customtkinter.CTkOptionMenu(self.sidebar, dynamic_resizing=False,
                                                        values=self.profile_name_list, command=self._select_profile)
        self.profile_menu.grid(row=2, column=0, padx=20, pady=(150, 10))
        if self.current_profile_id:
            self.profile_menu.set(self.profiles.get_profile_by_id(self.current_profile_id))

    def _refresh_path_list(self):
        for child in self.application_list_frame.winfo_children():
            child.destroy()
        self.application_list = []
        if self.current_profile_id:
            for path in self.profiles.get_paths_for_profile(self.current_profile_id):
                self._add_to_application_list(path)

    def _set_current_profile(self, current_profile):
        self.current_profile_id = current_profile
        self.settings.update_current_user_profile(current_profile)

    def _open_file_dialog(self):
        added_file = fd.askopenfilename()
        self._add_to_application_list(added_file)
        self.profiles.add_path_to_profile(self.current_profile_id, added_file)

    def _add_to_application_list(self, added_file):
        if added_file in self.application_list:
            print("File already in list")
            return
        self.application_list.append(added_file)
        label = customtkinter.CTkLabel(master=self.application_list_frame, text=added_file)
        label.grid(row=len(self.application_list) - 1, column=0, padx=10, pady=(0, 10), sticky="w")

    def _edit_profile(self):
        new_name = self._popup_input("Enter a New Profile Name", "Edit Profile", self.validate_new_profile_name)
        if new_name is None:
            return
        self._replace_value_in_profile_list(self.current_profile_id, new_name)
        self.profiles.change_profile_name(self.current_profile_id, new_name)
        self.profile_name_list = self.profiles.get_all_profile_names()
        self._refresh_profile_list()

    def _replace_value_in_profile_list(self, old_value, new_value):
        for i in range(len(self.profile_name_list)):
            if self.profile_name_list[i] == old_value:
                self.profile_name_list[i] = new_value

    def _get_window_geometry(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        window_x = (screen_width - WINDOW_WIDTH) // 2
        window_y = (screen_height - WINDOW_HEIGHT) // 2

        return f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}"

    def _popup_input(self, prompt, title, validation_func):
        text = prompt
        text_color = None
        x, y = self.winfo_pointerxy()
        _, _, position = self.geometry().partition("+")
        x_offset, y_offset = map(int, position.split("+"))
        dialog_x = max(0, x_offset + (x - x_offset) * 2)
        dialog_y = max(0, y_offset + (y - y_offset) // 1.5)
        dialog_geometry = f"300x150+{dialog_x}+{dialog_y}"
        while True:
            # TODO: Remove the try-catch block when a new version of customtkinter is released,
            # and the text_color issue is resolved.
            # in the meantime, line 34 of `venv/site-packages/customtkinter/windows/ctk_input_dialog.py`
            # has a typo at `button_hover_cover`, it should be `text_color`
            try:
                # Try to create the CTkInputDialog with text, title, and text_color
                self.dialog = customtkinter.CTkInputDialog(text=text, title=title, text_color=text_color)
            except Exception as e:
                if 'color is None' in e.args[0] and text_color is not None:
                    print("There was an error due to a typo in source code, "
                          "there is a pull request on the git repo for this")
                else:
                    print("Unknown error")

                child_list = []
                for child_name, child in self.children.items():
                    if isinstance(child, customtkinter.CTkInputDialog):
                        child_list.append(child)
                for child in child_list:
                    child.destroy()
                print("Attempting to print without `text_color`")
                self.dialog = customtkinter.CTkInputDialog(text=text, title=title)
            self.dialog.geometry(dialog_geometry)
            self.dialog.geometry(dialog_geometry)
            value = self.dialog.get_input()
            if value is None:
                return None
            error = validation_func(value)
            if error:
                text_color = "brown3"
                text = error
            else:
                return value

    def validate_new_profile_name(self, profile_name):
        if profile_name in self.profile_name_list:
            return "Profile name in use, enter a new one"
        if profile_name == "":
            return "Profile names cannot be empty"
        return None
