import hashlib
import streamlit as st
from config.database import DatabaseConnection
import sqlite3


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_user(username, password, user_type="teacher"):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        hashed_password = hash_password(password)

        if user_type == "admin":
            cursor.execute(
                "SELECT * FROM admin WHERE username = ? AND password = ?",
                (username, hashed_password),
            )
        else:
            cursor.execute(
                "SELECT * FROM teachers WHERE username = ? AND password = ? AND status = 'active'",
                (username, hashed_password),
            )

        user = cursor.fetchone()
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_type"] = user_type
            st.session_state["user_id"] = user[
                "admin_id" if user_type == "admin" else "teacher_id"
            ]
            st.session_state["username"] = user["username"]
            return True
        return False


def register_teacher(data):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO teachers (
                    username, password, first_name, last_name, email, phone,
                    age, qualification, joining_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["username"],
                    hash_password(data["password"]),
                    data["first_name"],
                    data["last_name"],
                    data["email"],
                    data["phone"],
                    data["age"],
                    data["qualification"],
                    data["joining_date"],
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def register_admin(data):
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO admin (
                    username, password, first_name, last_name,
                    age, qualification
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    data["username"],
                    hash_password(data["password"]),
                    data["first_name"],
                    data["last_name"],
                    data["age"],
                    data["qualification"],
                ),
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False


def check_auth():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("Please login to access this page")
        st.stop()
