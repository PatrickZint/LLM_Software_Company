import csv
import os
from config import CSV_EXPORT_DIR
from db import get_completions_for_habit


def export_habit_to_csv(habit_id, start_date=None, end_date=None):
    completions = get_completions_for_habit(habit_id, start_date, end_date)
    filename = os.path.join(CSV_EXPORT_DIR, f'habit_{habit_id}_export.csv')
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['id', 'habit_id', 'date', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for comp in completions:
            writer.writerow({
                'id': comp['id'],
                'habit_id': comp['habit_id'],
                'date': comp['date'],
                'timestamp': comp['timestamp']
            })
    return filename
