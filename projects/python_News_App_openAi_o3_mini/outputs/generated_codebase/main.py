import tkinter as tk
from config_manager import ConfigManager
from logger_setup import get_logger
from controller import Controller
from ui_home import HomeScreen


def main():
    # Initialize logger
    logger = get_logger(__name__)
    logger.info('Starting application...')

    # Load configuration
    try:
        config = ConfigManager('config.json')
    except Exception as e:
        print(f'Configuration error: {e}')
        return

    # Create main Tkinter window
    root = tk.Tk()
    root.title(config.get('app_title', 'News Reader'))
    root.geometry('800x600')

    # Initialize Controller and UI
    controller = Controller(config, logger)

    home_screen = HomeScreen(root, controller, logger)
    home_screen.pack(fill='both', expand=True)

    # Start application by fetching headlines
    controller.set_home_screen(home_screen)
    controller.fetch_headlines()

    # Kick off the mainloop
    root.mainloop()

if __name__ == '__main__':
    main()
