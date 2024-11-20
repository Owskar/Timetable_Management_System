from config.database import DatabaseConnection
from datetime import datetime, time


class TimetableHelper:
    @staticmethod
    def check_conflict(
        class_id, teacher_id, day, start_time, end_time, semester, exclude_id=None
    ):
        """Check for any scheduling conflicts"""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()

            # Convert times to strings for SQLite comparison
            start_str = start_time.strftime("%H:%M:%S")
            end_str = end_time.strftime("%H:%M:%S")

            # Check class schedule conflict
            cursor.execute(
                """
                SELECT * FROM timetable
                WHERE class_id = ? 
                AND day_of_week = ?
                AND semester = ?
                AND timetable_id != COALESCE(?, -1)
                AND (
                    (start_time <= ? AND end_time > ?) OR
                    (start_time < ? AND end_time >= ?) OR
                    (start_time >= ? AND end_time <= ?)
                )
            """,
                (
                    class_id,
                    day,
                    semester,
                    exclude_id,
                    start_str,
                    start_str,
                    end_str,
                    end_str,
                    start_str,
                    end_str,
                ),
            )

            if cursor.fetchone():
                return False, "Class schedule conflict"

            # Check teacher schedule conflict
            cursor.execute(
                """
                SELECT * FROM timetable
                WHERE teacher_id = ? 
                AND day_of_week = ?
                AND semester = ?
                AND timetable_id != COALESCE(?, -1)
                AND (
                    (start_time <= ? AND end_time > ?) OR
                    (start_time < ? AND end_time >= ?) OR
                    (start_time >= ? AND end_time <= ?)
                )
            """,
                (
                    teacher_id,
                    day,
                    semester,
                    exclude_id,
                    start_str,
                    start_str,
                    end_str,
                    end_str,
                    start_str,
                    end_str,
                ),
            )

            if cursor.fetchone():
                return False, "Teacher schedule conflict"

            return True, "No conflicts"

    @staticmethod
    def add_timetable_entry(
        class_id, teacher_id, subject_id, day, start_time, end_time, semester
    ):
        """Add a new timetable entry with validation"""
        # Check if the teacher teaches the subject
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT 1 FROM teacher_subjects
                WHERE teacher_id = ? AND subject_id = ?
            """,
                (teacher_id, subject_id),
            )

            if not cursor.fetchone():
                return False, "Teacher is not assigned to this subject"

            # Check for conflicts
            is_valid, message = TimetableHelper.check_conflict(
                class_id, teacher_id, day, start_time, end_time, semester
            )

            if not is_valid:
                return False, message

            # Add entry
            try:
                cursor.execute(
                    """
                    INSERT INTO timetable (
                        class_id, teacher_id, subject_id, day_of_week,
                        start_time, end_time, semester
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        class_id,
                        teacher_id,
                        subject_id,
                        day,
                        start_time,
                        end_time,
                        semester,
                    ),
                )
                conn.commit()
                return True, "Timetable entry added successfully"
            except Exception as e:
                return False, f"Error adding entry: {str(e)}"

    @staticmethod
    def get_class_timetable(class_id, semester):
        """Get timetable for a specific class"""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, s.subject_name, 
                       tc.first_name as teacher_first_name,
                       tc.last_name as teacher_last_name
                FROM timetable t
                JOIN subjects s ON t.subject_id = s.subject_id
                JOIN teachers tc ON t.teacher_id = tc.teacher_id
                WHERE t.class_id = ? AND t.semester = ?
                ORDER BY 
                    CASE t.day_of_week
                        WHEN 'Monday' THEN 1
                        WHEN 'Tuesday' THEN 2
                        WHEN 'Wednesday' THEN 3
                        WHEN 'Thursday' THEN 4
                        WHEN 'Friday' THEN 5
                        WHEN 'Saturday' THEN 6
                    END,
                    t.start_time
            """,
                (class_id, semester),
            )
            return cursor.fetchall()

    @staticmethod
    def get_teacher_timetable(teacher_id, semester):
        """Get timetable for a specific teacher"""
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT t.*, s.subject_name, c.class_name
                FROM timetable t
                JOIN subjects s ON t.subject_id = s.subject_id
                JOIN classes c ON t.class_id = c.class_id
                WHERE t.teacher_id = ? AND t.semester = ?
                ORDER BY 
                    CASE t.day_of_week
                        WHEN 'Monday' THEN 1
                        WHEN 'Tuesday' THEN 2
                        WHEN 'Wednesday' THEN 3
                        WHEN 'Thursday' THEN 4
                        WHEN 'Friday' THEN 5
                        WHEN 'Saturday' THEN 6
                    END,
                    t.start_time
            """,
                (teacher_id, semester),
            )
            return cursor.fetchall()
