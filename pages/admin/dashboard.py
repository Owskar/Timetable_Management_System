import streamlit as st
from utils.auth_helper import check_auth
from config.database import DatabaseConnection
import sqlite3


def manage_teachers():
    st.subheader("Manage Teachers")

    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM teachers")
        teachers = cursor.fetchall()

        # Display teachers in a table
        if teachers:
            teacher_data = []
            for teacher in teachers:
                teacher_data.append(
                    {
                        "ID": teacher["teacher_id"],
                        "Name": f"{teacher['first_name']} {teacher['last_name']}",
                        "Email": teacher["email"],
                        "Status": teacher["status"],
                    }
                )

            st.table(teacher_data)

            # Edit/Delete teacher
            teacher_id = st.number_input("Enter Teacher ID to edit/delete", min_value=1)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Delete Teacher"):
                    cursor.execute(
                        "UPDATE teachers SET status = 'inactive' WHERE teacher_id = ?",
                        (teacher_id,),
                    )
                    conn.commit()
                    st.success("Teacher deactivated successfully!")
                    st.rerun()

            with col2:
                if st.button("Edit Teacher"):
                    cursor.execute(
                        "SELECT * FROM teachers WHERE teacher_id = ?", (teacher_id,)
                    )
                    teacher = cursor.fetchone()
                    if teacher:
                        with st.form("edit_teacher"):
                            first_name = st.text_input(
                                "First Name", teacher["first_name"]
                            )
                            last_name = st.text_input("Last Name", teacher["last_name"])
                            email = st.text_input("Email", teacher["email"])
                            phone = st.text_input("Phone", teacher["phone"])
                            status = st.selectbox(
                                "Status",
                                ["active", "inactive"],
                                0 if teacher["status"] == "active" else 1,
                            )

                            if st.form_submit_button("Update"):
                                cursor.execute(
                                    """
                                    UPDATE teachers 
                                    SET first_name = ?, last_name = ?, email = ?, phone = ?, status = ?
                                    WHERE teacher_id = ?
                                """,
                                    (
                                        first_name,
                                        last_name,
                                        email,
                                        phone,
                                        status,
                                        teacher_id,
                                    ),
                                )
                                conn.commit()
                                st.success("Teacher updated successfully!")
                                st.rerun()


def manage_subjects():
    st.subheader("Manage Subjects")

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Add new subject
        with st.form("add_subject"):
            st.write("Add New Subject")
            subject_code = st.text_input("Subject Code")
            subject_name = st.text_input("Subject Name")
            description = st.text_area("Description")
            credits = st.number_input("Credits", min_value=1)

            if st.form_submit_button("Add Subject"):
                try:
                    cursor.execute(
                        """
                        INSERT INTO subjects (subject_code, subject_name, description, credits)
                        VALUES (?, ?, ?, ?)
                    """,
                        (subject_code, subject_name, description, credits),
                    )
                    conn.commit()
                    st.success("Subject added successfully!")
                except sqlite3.IntegrityError:
                    st.error("Subject code already exists!")

        # Display and manage existing subjects
        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()

        # if subjects:


########################################################################
def manage_classes():
    st.subheader("Manage Classes")

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Add new class
        with st.form("add_class"):
            st.write("Add New Class")
            class_name = st.text_input("Class Name")
            grade_level = st.number_input("Grade Level", min_value=1, max_value=12)
            section = st.text_input("Section")
            academic_year = st.text_input("Academic Year (YYYY-YYYY)")
            room_number = st.text_input("Room Number")
            capacity = st.number_input("Capacity", min_value=1)

            if st.form_submit_button("Add Class"):
                try:
                    cursor.execute(
                        """
                        INSERT INTO classes (class_name, grade_level, section, academic_year, room_number, capacity)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """,
                        (
                            class_name,
                            grade_level,
                            section,
                            academic_year,
                            room_number,
                            capacity,
                        ),
                    )
                    conn.commit()
                    st.success("Class added successfully!")
                except sqlite3.IntegrityError:
                    st.error("Class combination already exists!")

        # Display and manage existing classes
        cursor.execute("SELECT * FROM classes")
        classes = cursor.fetchall()

        if classes:
            st.write("Existing Classes")
            class_data = []
            for class_ in classes:
                class_data.append(
                    {
                        "ID": class_["class_id"],
                        "Name": class_["class_name"],
                        "Grade": class_["grade_level"],
                        "Section": class_["section"],
                        "Year": class_["academic_year"],
                    }
                )

            st.table(class_data)

            # Edit/Delete class
            class_id = st.number_input("Enter Class ID to edit/delete", min_value=1)
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Delete Class"):
                    cursor.execute(
                        "DELETE FROM classes WHERE class_id = ?", (class_id,)
                    )
                    conn.commit()
                    st.success("Class deleted successfully!")
                    st.rerun()

            with col2:
                if st.button("Edit Class"):
                    cursor.execute(
                        "SELECT * FROM classes WHERE class_id = ?", (class_id,)
                    )
                    class_ = cursor.fetchone()
                    if class_:
                        with st.form("edit_class"):
                            class_name = st.text_input(
                                "Class Name", class_["class_name"]
                            )
                            grade_level = st.number_input(
                                "Grade Level",
                                min_value=1,
                                max_value=12,
                                value=class_["grade_level"],
                            )
                            section = st.text_input("Section", class_["section"])
                            academic_year = st.text_input(
                                "Academic Year", class_["academic_year"]
                            )
                            room_number = st.text_input(
                                "Room Number", class_["room_number"]
                            )
                            capacity = st.number_input(
                                "Capacity", min_value=1, value=class_["capacity"]
                            )

                            if st.form_submit_button("Update"):
                                cursor.execute(
                                    """
                                    UPDATE classes 
                                    SET class_name = ?, grade_level = ?, section = ?, 
                                        academic_year = ?, room_number = ?, capacity = ?
                                    WHERE class_id = ?
                                """,
                                    (
                                        class_name,
                                        grade_level,
                                        section,
                                        academic_year,
                                        room_number,
                                        capacity,
                                        class_id,
                                    ),
                                )
                                conn.commit()
                                st.success("Class updated successfully!")
                                st.rerun()


def generate_timetable():
    st.subheader("Generate Timetable")

    with DatabaseConnection() as conn:
        cursor = conn.cursor()

        # Get all classes, teachers, and subjects
        cursor.execute("SELECT * FROM classes")
        classes = cursor.fetchall()

        cursor.execute("SELECT * FROM teachers WHERE status = 'active'")
        teachers = cursor.fetchall()

        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()

        # Form to add timetable entry
        with st.form("add_timetable"):
            class_id = st.selectbox(
                "Select Class",
                options=[c["class_id"] for c in classes],
                format_func=lambda x: next(
                    c["class_name"] for c in classes if c["class_id"] == x
                ),
            )

            teacher_id = st.selectbox(
                "Select Teacher",
                options=[t["teacher_id"] for t in teachers],
                format_func=lambda x: f"{next(t['first_name'] for t in teachers if t['teacher_id'] == x)} {next(t['last_name'] for t in teachers if t['teacher_id'] == x)}",
            )

            subject_id = st.selectbox(
                "Select Subject",
                options=[s["subject_id"] for s in subjects],
                format_func=lambda x: next(
                    s["subject_name"] for s in subjects if s["subject_id"] == x
                ),
            )

            day = st.selectbox(
                "Day",
                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            )
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
            semester = st.number_input("Semester", min_value=1, max_value=2)

            if st.form_submit_button("Add to Timetable"):
                try:
                    cursor.execute(
                        """
                        INSERT INTO timetable (class_id, teacher_id, subject_id, day_of_week, start_time, end_time, semester)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
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
                    st.success("Timetable entry added successfully!")
                except sqlite3.IntegrityError:
                    st.error("This time slot is already occupied!")

        # Display existing timetable
        cursor.execute(
            """
            SELECT t.*, c.class_name, tc.first_name, tc.last_name, s.subject_name
            FROM timetable t
            JOIN classes c ON t.class_id = c.class_id
            JOIN teachers tc ON t.teacher_id = tc.teacher_id
            JOIN subjects s ON t.subject_id = s.subject_id
            ORDER BY t.day_of_week, t.start_time
        """
        )
        timetable = cursor.fetchall()

        if timetable:
            st.write("Current Timetable")
            timetable_data = []
            for entry in timetable:
                timetable_data.append(
                    {
                        "ID": entry["timetable_id"],
                        "Class": entry["class_name"],
                        "Teacher": f"{entry['first_name']} {entry['last_name']}",
                        "Subject": entry["subject_name"],
                        "Day": entry["day_of_week"],
                        "Time": f"{entry['start_time']} - {entry['end_time']}",
                        "Semester": entry["semester"],
                    }
                )

            st.table(timetable_data)

            # Delete timetable entry
            entry_id = st.number_input(
                "Enter Timetable Entry ID to delete", min_value=1
            )
            if st.button("Delete Entry"):
                cursor.execute(
                    "DELETE FROM timetable WHERE timetable_id = ?", (entry_id,)
                )
                conn.commit()
                st.success("Timetable entry deleted successfully!")
                st.rerun()


def show_admin_dashboard():
    check_auth()

    st.title("Admin Dashboard")

    menu = [
        "Manage Teachers",
        "Manage Subjects",
        "Manage Classes",
        "Generate Timetable",
    ]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Manage Teachers":
        manage_teachers()
    elif choice == "Manage Subjects":
        manage_subjects()
    elif choice == "Manage Classes":
        manage_classes()
    elif choice == "Generate Timetable":
        generate_timetable()
