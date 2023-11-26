# Workspace-Viewer
An automation script for launching a predefined set of computer applications on Windows.

# How to Use
For running main.py, you can use the included Pipfile to install all required dependencies:

### Install pipenv
``
pip3 install pipenv
``

### Install packages
``
pipenv install
``

# Description
The application gives the user the ability to create profiles which each contain a set of applications.
These profiles can have applications added and removed from them, and when the user presses the "Launch Profile"
button, all the applications associated with that profile will be launched.

### Why not just use Task Manager / Windows?
Having different profiles allows you to choose what your PC is starting up as. Work? Gaming? Casual browsing?
Controlling your profiles will ensure that no unneeded applications are started in the background unless you intend to use them.

### Todo / Ideas / Nice to have
Open on Startup
Select a profile to launch on startup
Generalized support for files that are not `.exe` files
Selenium
