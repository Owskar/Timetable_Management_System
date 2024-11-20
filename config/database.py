import sqlite3
import os
from datetime import datetime


class DatabaseConnection:
    def __init__(self, db_file="database.db"):
        self.db_file = db_file

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()


def init_db():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Create admin table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS admin (
            admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER,
            qualification TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Create teachers table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            age INTEGER,
            qualification TEXT,
            joining_date DATE NOT NULL,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Create subjects table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS subjects (
            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_code TEXT UNIQUE NOT NULL,
            subject_name TEXT NOT NULL,
            description TEXT,
            credits INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Create classes table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS classes (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT NOT NULL,
            grade_level INTEGER NOT NULL,
            section TEXT NOT NULL,
            academic_year TEXT NOT NULL,
            room_number TEXT,
            capacity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(grade_level, section, academic_year)
        )
        """
        )

        # Create teacher_subjects table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS teacher_subjects (
            teacher_subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
            UNIQUE(teacher_id, subject_id)
        )
        """
        )

        # Create timetable table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS timetable (
            timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            teacher_id INTEGER NOT NULL,
            subject_id INTEGER NOT NULL,
            day_of_week TEXT NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            semester INTEGER NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (class_id) REFERENCES classes(class_id),
            FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id),
            FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        )
        """
        )

        conn.commit()


def check_admin_exists():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM admin")
        result = cursor.fetchone()
        return result["count"] > 0
