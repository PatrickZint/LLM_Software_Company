import gui
import db


def main():
    # Initialize the database (for logging or future use)
    db.init_db()
    # Launch the GUI application
    app = gui.ImageDiffGUI()
    app.mainloop()


if __name__ == '__main__':
    main()
