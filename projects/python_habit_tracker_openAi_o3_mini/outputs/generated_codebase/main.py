from db import init_db
from gui import HabitTrackerGUI


def main():
    # Initialize the database and tables
    init_db()
    
    # Launch the Habit Tracker GUI
    app = HabitTrackerGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
