import streamlit as st


def init_session():
    """Initialize session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_type" not in st.session_state:
        st.session_state["user_type"] = None
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None


def clear_session():
    """Clear all session state variables"""
    st.session_state["logged_in"] = False
    st.session_state["user_type"] = None
