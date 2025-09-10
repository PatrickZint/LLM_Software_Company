import os

# Configuration for the Habit Tracking Application

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'habit_tracker.db')
CSV_EXPORT_DIR = os.path.join(BASE_DIR, 'exports')

if not os.path.exists(CSV_EXPORT_DIR):
    os.makedirs(CSV_EXPORT_DIR)
