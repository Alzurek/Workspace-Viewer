import customtkinter
from tkinter import filedialog as fd

class Interface(customtkinter.CTk):
    selected_profile: str

    def __init__(self):
        super().__init__()

        self.geometry(f"{900}x{550}")

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
                                                             command=self.create_profile)
        self.create_profile_button.grid(row=1, column=0, padx=20, pady=10)
        self.launch_profile_button = customtkinter.CTkButton(self.sidebar, text="Launch Profile",
                                                             command=self.launch_profile)
        self.launch_profile_button.grid(row=2, column=0, padx=20, pady=10)
        self.profile_menu = customtkinter.CTkOptionMenu(self.sidebar, dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"],
                                                        command=self.select_profile)
        self.profile_menu.grid(row=2, column=0, padx=20, pady=(100, 10))
        # GUI Theme
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_option_menu = customtkinter.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_option_menu.grid(row=6, column=0, padx=20, pady=(10, 30))
        # Set following based on saved data
        self.appearance_mode_option_menu.set("Dark")

        self.entry = customtkinter.CTkButton(self, text="Choose Application", command=self.open_file_dialog)
        self.entry.grid(row=0, column=1, padx=20, pady=20, sticky="n")

        self.application_list = customtkinter.CTkScrollableFrame(self, label_text="Applications to Launch")
        self.application_list.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

    def select_profile(self, new_profile: str):
        self.selected_profile = new_profile
        print("Updated profile")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        # Save data

    def launch_profile(self):
        print(f"Launching profile {self.selected_profile}")

    def create_profile(self):
        print(f"create profile")

    def open_file_dialog(self):
        added_file = fd.askopenfilename()
        print(added_file)
