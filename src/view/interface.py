import customtkinter
import tkinter as tk
from tkinter import filedialog as fd
from src.service.settings_service import SettingsService

WINDOW_HEIGHT = 550
WINDOW_WIDTH = 900
DEFAULT_APPEARANCE = "Dark"


class Interface(customtkinter.CTk):
    selected_profile: str

    def __init__(self):
        super().__init__()
        window_geometry = self._get_window_geometry()

        self.settings = SettingsService()
        self.current_appearance = self.settings.get_user_app_appearance()
        if self.current_appearance is None:
            self.current_appearance = DEFAULT_APPEARANCE
        self.geometry(window_geometry)

        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure(1, weight=1)

        # Create sidebar
        self.sidebar = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar.grid_rowconfigure(3, weight=1)
        # Profile Select
        self.title_label = customtkinter.CTkLabel(self.sidebar, text="Application Launcher",
                                                  font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.create_profile_button = customtkinter.CTkButton(self.sidebar, text="Create Profile",
                                                             command=self._create_profile)
        self.create_profile_button.grid(row=1, column=0, padx=20, pady=10)
        self.launch_profile_button = customtkinter.CTkButton(self.sidebar, text="Launch Profile",
                                                             command=self._launch_profile)
        self.launch_profile_button.grid(row=2, column=0, padx=20, pady=10)
        self.profile_menu = customtkinter.CTkOptionMenu(self.sidebar, dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"],
                                                        command=self._select_profile)
        self.profile_menu.grid(row=2, column=0, padx=20, pady=(100, 10))
        # GUI Theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                                       command=self._change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 30))
        # Set following based on saved data
        self.appearance_mode_option_menu.set(self.current_appearance)
        customtkinter.set_appearance_mode(self.current_appearance)

        self.entry = customtkinter.CTkButton(self, text="Choose Application", command=self._open_file_dialog)
        self.entry.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.application_list = customtkinter.CTkScrollableFrame(self, label_text="Applications to Launch")
        self.application_list.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def _select_profile(self, new_profile: str):
        self.selected_profile = new_profile
        print("Updated profile")

    def _change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.settings.update_user_app_appearance(new_appearance_mode)

    def _launch_profile(self):
        print(f"Launching profile {self.selected_profile}")

    def _create_profile(self):
        print(f"create profile")

    def _open_file_dialog(self):
        added_file = fd.askopenfilename()
        print(added_file)

    def _get_window_geometry(self):
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.destroy()

        window_x = (screen_width - WINDOW_WIDTH) // 2
        window_y = (screen_height - WINDOW_HEIGHT) // 2

        return f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{window_x}+{window_y}"
