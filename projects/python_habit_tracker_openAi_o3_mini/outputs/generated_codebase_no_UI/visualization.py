import matplotlib.pyplot as plt
import sqlite3
from database import get_connection


def plot_habit_progress(habit_id):
    """
    Generate a simple bar chart showing habit completion counts by date for the given habit_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT log_date, COUNT(*) as count 
        FROM habit_log
        WHERE habit_id = ? AND status = 'completed'
        GROUP BY log_date
        ORDER BY log_date
    ''', (habit_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print('No logs found for habit_id:', habit_id)
        return

    dates = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.bar(dates, counts, color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Completion Count')
    plt.title(f'Habit Progress for Habit ID: {habit_id}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def plot_habit_progress_line(habit_id):
    """
    Generate a line chart for the habit completion over time.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT log_date, COUNT(*) as count 
        FROM habit_log
        WHERE habit_id = ? AND status = 'completed'
        GROUP BY log_date
        ORDER BY log_date
    ''', (habit_id,))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print('No logs found for habit_id:', habit_id)
        return

    dates = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, counts, marker='o', linestyle='-', color='green')
    plt.xlabel('Date')
    plt.ylabel('Completion Count')
    plt.title(f'Habit Progress (Line Chart) for Habit ID: {habit_id}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
