# Running this application opens a GUI that allows the user to edit their paths, make profiles, and launch profiles
from src.view.interface import Interface

inter = Interface()
inter.mainloop()

# Edit Paths:
#       File is made/updated when new paths are added
#       profiles are defined as different files (name of file is name of profile)


# Launch profile:
#       Read in paths from file
#       For each path, execute (open)


# Ideas / Nice to Haves:
#       Open on Startup
#       Select a profile to launch on startup

