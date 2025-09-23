import sqlite3
import os
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._initialize_tables()

    def _connect(self):
        self.conn = sqlite3.connect(self.db_path)

    def _initialize_tables(self):
        cursor = self.conn.cursor()
        # Table for storing image metadata and comparison details
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS comparisons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image1_path TEXT,
                image2_path TEXT,
                image1_dims TEXT,
                image2_dims TEXT,
                tolerance INTEGER,
                difference_score REAL,
                timestamp TEXT
            )
        ''')
        self.conn.commit()

    def log_comparison(self, image1_path, image2_path, image1_dims, image2_dims, tolerance, difference_score):
        cursor = self.conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO comparisons (
                image1_path, image2_path, image1_dims, image2_dims, tolerance, difference_score, timestamp
            ) VALUES (?,?,?,?,?,?,?)
        ''', (image1_path, image2_path, str(image1_dims), str(image2_dims), tolerance, difference_score, timestamp))
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()


if __name__ == '__main__':
    # Quick test
    db = DatabaseManager('test.db')
    db.log_comparison('img1.png', 'img2.png', (800,600), (800,600), 10, 12345)
    db.close()
