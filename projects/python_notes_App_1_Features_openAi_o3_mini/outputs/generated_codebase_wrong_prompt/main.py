from db import init_db
from app import NoteApp


def main():
    # Initialize the database (creates tables if not exist)
    init_db()
    
    # Start the Note Taking Application
    app = NoteApp()
    app.mainloop()


if __name__ == '__main__':
    main()