import csv
from database import get_connection


def export_habit_data(filepath, habit_id=None):
    """
    Export habit data and their logs to a CSV file.
    If habit_id is provided, export only that habit's data;
    otherwise, export data for all habits.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if habit_id:
        cursor.execute('''
            SELECT h.id, h.title, h.description, h.goal, h.schedule, h.start_date, h.end_date, h.category, l.log_date, l.status, l.notes
            FROM habit h
            LEFT JOIN habit_log l ON h.id = l.habit_id
            WHERE h.id = ?
            ORDER BY l.log_date
        ''', (habit_id,))
    else:
        cursor.execute('''
            SELECT h.id, h.title, h.description, h.goal, h.schedule, h.start_date, h.end_date, h.category, l.log_date, l.status, l.notes
            FROM habit h
            LEFT JOIN habit_log l ON h.id = l.habit_id
            ORDER BY h.id, l.log_date
        ''')

    rows = cursor.fetchall()
    conn.close()

    header = ['Habit ID', 'Title', 'Description', 'Goal', 'Schedule', 'Start Date', 'End Date', 'Category', 'Log Date', 'Status', 'Notes']
    
    with open(filepath, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    print(f'Data exported successfully to {filepath}')
