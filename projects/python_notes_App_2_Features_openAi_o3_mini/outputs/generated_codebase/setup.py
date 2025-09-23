from setuptools import setup, find_packages

setup(
    name="note_taking_app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "note_taking_app = main:main"
        ]
    },
    author="Your Name",
    description="A simple note taking app using Python, Tkinter, and SQLite for local storage."
)
