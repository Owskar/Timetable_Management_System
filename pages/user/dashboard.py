import streamlit as st
from utils.auth_helper import check_auth
from config.database import DatabaseConnection


def show_profile():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, GROUP_CONCAT(s.subject_name) as subjects
            FROM teachers t
            LEFT JOIN teacher_subjects ts ON t.teacher_id = ts.teacher_id
            LEFT JOIN subjects s ON ts.subject_id = s.subject_id
            WHERE t.teacher_id = ?
            GROUP BY t.teacher_id
        """,
            (st.session_state["user_id"],),
        )
        teacher = cursor.fetchone()

        if teacher:
            st.write("### Personal Information")
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Name:** {teacher['first_name']} {teacher['last_name']}")
                st.write(f"**Email:** {teacher['email']}")
                st.write(f"**Phone:** {teacher['phone']}")

            with col2:
                st.write(f"**Age:** {teacher['age']}")
                st.write(f"**Qualification:** {teacher['qualification']}")
                st.write(f"**Joining Date:** {teacher['joining_date']}")

            if teacher["subjects"]:
                st.write("**Teaching Subjects:**", teacher["subjects"])

            # Edit profile
            if st.button("Edit Profile"):
                with st.form("edit_profile"):
                    phone = st.text_input("Phone", teacher["phone"])
                    email = st.text_input("Email", teacher["email"])

                    if st.form_submit_button("Update Profile"):
                        cursor.execute(
                            """
                            UPDATE teachers 
                            SET phone = ?, email = ?
                            WHERE teacher_id = ?
                        """,
                            (phone, email, st.session_state["user_id"]),
                        )
                        conn.commit()
                        st.success("Profile updated successfully!")
                        st.rerun()


def show_timetable():
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT t.*, c.class_name, s.subject_name
            FROM timetable t
            JOIN classes c ON t.class_id = c.class_id
            JOIN subjects s ON t.subject_id = s.subject_id
            WHERE t.teacher_id = ? AND t.is_active = 1
            ORDER BY 
                CASE 
                    WHEN t.day_of_week = 'Monday' THEN 1
                    WHEN t.day_of_week = 'Tuesday' THEN 2
                    WHEN t.day_of_week = 'Wednesday' THEN 3
                    WHEN t.day_of_week = 'Thursday' THEN 4
                    WHEN t.day_of_week = 'Friday' THEN 5
                    WHEN t.day_of_week = 'Saturday' THEN 6
                END,
                t.start_time
        """,
            (st.session_state["user_id"],),
        )
        schedule = cursor.fetchall()

        if schedule:
            st.write("### My Teaching Schedule")

            # Group by day
            schedule_by_day = {}
            for entry in schedule:
                day = entry["day_of_week"]
                if day not in schedule_by_day:
                    schedule_by_day[day] = []
                schedule_by_day[day].append(entry)

            # Display schedule
            for day in [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]:
                if day in schedule_by_day:
                    st.write(f"**{day}**")
                    for entry in schedule_by_day[day]:
                        st.write(
                            f"{entry['start_time']} - {entry['end_time']}: {entry['subject_name']} ({entry['class_name']})"
                        )
        else:
            st.info("No classes scheduled")


def show_user_dashboard():
    check_auth()

    st.title(f"Welcome, {st.session_state['username']}")

    menu = ["My Profile", "My Schedule"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "My Profile":
        show_profile()
    elif choice == "My Schedule":
        show_timetable()
