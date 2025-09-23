import csv
import sqlite3


def export_logs_to_csv(db_path, export_path, start_date=None, end_date=None, rule_filter=None):
    """
    Exports logs from the database to a CSV file with optional filtering by date range and rule.
    Dates should be in ISO format strings (e.g., '2023-01-01T00:00:00').
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = "SELECT original_path, destination_path, timestamp, sorting_rule FROM file_logs WHERE 1=1"
    params = []
    if start_date:
        query += " AND timestamp >= ?"
        params.append(start_date)
    if end_date:
        query += " AND timestamp <= ?"
        params.append(end_date)
    if rule_filter:
        query += " AND sorting_rule = ?"
        params.append(rule_filter)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    try:
        with open(export_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['original_path', 'destination_path', 'timestamp', 'sorting_rule'])
            writer.writerows(rows)
        print(f"Logs exported successfully to {export_path}")
    except Exception as e:
        print(f"Failed to export CSV logs: {e}")
