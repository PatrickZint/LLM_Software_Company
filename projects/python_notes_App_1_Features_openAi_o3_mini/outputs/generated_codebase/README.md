# Simple Note-Taking Application

This is a simple note-taking application built with Python and Tkinter. It allows users to create, view, edit, and delete personal notes.

## Features

- Create a new note with a title and content.
- View a list of existing notes, sorted by the last updated timestamp.
- Edit an existing note.
- Delete a note with a confirmation prompt.
- Persistent storage using a local JSON file (`notes.json`).

## Requirements

- Python 3.9 or later
- Tkinter (usually comes bundled with Python)

## Installation

1. Make sure you have Python 3.9+ installed. You can check your Python version with:

   ```bash
   python --version
   ```

2. Clone the repository or download the source files.

3. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Run the application:

   ```bash
   python main.py
   ```

## File Structure

- `main.py`: The main entry point for the GUI application.
- `note.py`: Contains the `create_note_dict` function for creating note objects.
- `note_manager.py`: Contains the `NoteManager` class that manages note operations and data persistence.
- `notes.json`: A JSON file that stores the notes data (created automatically when a note is added).

## Future Enhancements

- Add tagging or categorization for notes.
- Implement search functionality.
- Improve the UI styling and responsiveness.
- Add unit and integration tests for better code coverage.
