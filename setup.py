"""Package configuration for Workspace Viewer.

This module defines the package metadata and dependencies.
"""
from setuptools import setup, find_packages

setup(
    name="workspace-viewer",
    version="0.1",
    packages=find_packages(include=['src', 'src.*', 'test', 'test.*']),
    package_dir={'': '.'},
    install_requires=[
        "customtkinter",
        "packaging",
        "pillow",
    ],
    python_requires='>=3.7',
)
