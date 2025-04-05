"""Main entry point for the Workspace Viewer application.

This module initializes and runs the main GUI window.
Running this application opens a GUI that allows the user to edit their paths, make profiles, and
launch profiles.
"""
from src.view.interface import UserInterface

inter = UserInterface()
inter.mainloop()
