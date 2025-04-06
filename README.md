# Workspace-Viewer
![Pylint](https://github.com/Alzurek/Workspace-Viewer/actions/workflows/pylint.yml/badge.svg)
![Pytest](https://github.com/Alzurek/Workspace-Viewer/actions/workflows/pytest.yml/badge.svg)
[![codecov](https://codecov.io/gh/Alzurek/Workspace-Viewer/branch/main/graph/badge.svg)](https://codecov.io/gh/Alzurek/Workspace-Viewer)

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

### Creating .exe
``
pyinstaller --name="Application Viewer" --onefile --noconsole --icon=.\resource\logo.ico main.py
``

### Linting
``
pylint src
``

### Testing
Run tests with coverage reporting:
``
pytest --cov=src --cov-report=xml --cov-report=term-missing
``

For coverage highlighting in VSCode:
1. Install the "Coverage Gutters" extension
2. Run the above command to generate coverage.xml
3. Use the command palette (Ctrl+Shift+P):
   - "Coverage Gutters: Watch" to start coverage highlighting
   - "Coverage Gutters: Toggle" to show/hide the coverage

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
