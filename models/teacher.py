from config.database import DatabaseConnection


class TeacherSubject:
    @staticmethod
    def assign_subject(teacher_id, subject_id):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    INSERT INTO teacher_subjects (teacher_id, subject_id)
                    VALUES (?, ?)
                """,
                    (teacher_id, subject_id),
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"Error assigning subject: {e}")
                return False

    @staticmethod
    def remove_subject(teacher_id, subject_id):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    """
                    DELETE FROM teacher_subjects
                    WHERE teacher_id = ? AND subject_id = ?
                """,
                    (teacher_id, subject_id),
                )
                conn.commit()
                return True
            except Exception as e:
                print(f"Error removing subject: {e}")
                return False

    @staticmethod
    def get_teacher_subjects(teacher_id):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT s.* 
                FROM subjects s
                JOIN teacher_subjects ts ON s.subject_id = ts.subject_id
                WHERE ts.teacher_id = ?
            """,
                (teacher_id,),
            )
            return cursor.fetchall()

    @staticmethod
    def get_available_subjects(teacher_id):
        with DatabaseConnection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT * FROM subjects 
                WHERE subject_id NOT IN (
                    SELECT subject_id 
                    FROM teacher_subjects 
                    WHERE teacher_id = ?
                )
            """,
                (teacher_id,),
            )
            return cursor.fetchall()
