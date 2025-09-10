import sqlite3
from database import get_connection
from models import Habit, HabitLog


def create_habit(title, description, goal, schedule, start_date, end_date=None, category=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO habit (title, description, goal, schedule, start_date, end_date, category) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (title, description, goal, schedule, start_date, end_date, category))
    conn.commit()
    habit_id = cursor.lastrowid
    conn.close()
    return habit_id


def update_habit(habit_id, title=None, description=None, goal=None, schedule=None, start_date=None, end_date=None, category=None):
    conn = get_connection()
    cursor = conn.cursor()
    # Build update query dynamically
    fields = []
    values = []
    if title is not None:
        fields.append('title = ?')
        values.append(title)
    if description is not None:
        fields.append('description = ?')
        values.append(description)
    if goal is not None:
        fields.append('goal = ?')
        values.append(goal)
    if schedule is not None:
        fields.append('schedule = ?')
        values.append(schedule)
    if start_date is not None:
        fields.append('start_date = ?')
        values.append(start_date)
    if end_date is not None:
        fields.append('end_date = ?')
        values.append(end_date)
    if category is not None:
        fields.append('category = ?')
        values.append(category)

    values.append(habit_id)
    sql = f"UPDATE habit SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, values)
    conn.commit()
    conn.close()


def delete_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM habit WHERE id = ?', (habit_id,))
    conn.commit()
    conn.close()


def get_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, goal, schedule, start_date, end_date, category FROM habit WHERE id = ?', (habit_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Habit(*row)
    return None


def get_all_habits():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, description, goal, schedule, start_date, end_date, category FROM habit')
    rows = cursor.fetchall()
    conn.close()
    habits = [Habit(*row) for row in rows]
    return habits


def log_habit_completion(habit_id, log_date, status='completed', notes=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO habit_log (habit_id, log_date, status, notes)
        VALUES (?, ?, ?, ?)
    ''', (habit_id, log_date, status, notes))
    conn.commit()
    log_id = cursor.lastrowid
    conn.close()
    return log_id


def get_logs_for_habit(habit_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, habit_id, log_date, status, notes FROM habit_log WHERE habit_id = ? ORDER BY log_date', (habit_id,))
    rows = cursor.fetchall()
    conn.close()
    logs = [HabitLog(*row) for row in rows]
    return logs
