import streamlit as st
from config.database import init_db, check_admin_exists
from utils.auth_helper import login_user, register_teacher, register_admin
import datetime


def main():
    st.set_page_config(page_title="Timetable Management System", layout="wide")
    init_db()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        st.title("Welcome to Timetable Management System")

        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            st.subheader("Login")
            login_type = st.radio("Select Login Type", ["Teacher", "Admin"])
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if login_user(
                    username, password, "admin" if login_type == "Admin" else "teacher"
                ):
                    st.success("Logged in successfully!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        with tab2:
            st.subheader("Sign Up")
            signup_type = st.radio("Select Sign Up Type", ["Teacher", "Admin"])

            if signup_type == "Admin" and check_admin_exists():
                st.error("Admin account already exists")
            else:
                with st.form("signup_form"):
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    first_name = st.text_input("First Name")
                    last_name = st.text_input("Last Name")
                    age = st.number_input("Age", min_value=18, max_value=100)
                    qualification = st.text_input("Qualification")

                    if signup_type == "Teacher":
                        email = st.text_input("Email")
                        phone = st.text_input("Phone")
                        joining_date = st.date_input("Joining Date")

                    if st.form_submit_button("Sign Up"):
                        if signup_type == "Teacher":
                            data = {
                                "username": username,
                                "password": password,
                                "first_name": first_name,
                                "last_name": last_name,
                                "email": email,
                                "phone": phone,
                                "age": age,
                                "qualification": qualification,
                                "joining_date": joining_date,
                            }
                            if register_teacher(data):
                                st.success("Teacher registered successfully!")
                            else:
                                st.error("Username or email already exists")
                        else:
                            data = {
                                "username": username,
                                "password": password,
                                "first_name": first_name,
                                "last_name": last_name,
                                "age": age,
                                "qualification": qualification,
                            }
                            if register_admin(data):
                                st.success("Admin registered successfully!")
                            else:
                                st.error("Username already exists")
    else:
        if st.session_state["user_type"] == "admin":
            from pages.admin.dashboard import show_admin_dashboard

            show_admin_dashboard()
        else:
            from pages.user.dashboard import show_user_dashboard

            show_user_dashboard()

        if st.sidebar.button("Logout"):
            st.session_state["logged_in"] = False
            st.rerun()


if __name__ == "__main__":
    main()
