import streamlit as st
from database.db import get_connection


def create_user_table():
    """
    Creates users table if it does not already exist.
    Also creates one default admin account if no admin exists.
    """
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

    default_user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    ).fetchone()

    if not default_user:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "HR")
        )
        conn.commit()

    conn.close()


def login_form():
    create_user_table()

    st.subheader("HR Authentication")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ---------------- LOGIN TAB ----------------
    with tab1:
        st.markdown("### Login")

        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")

        st.info("Default Login: admin / admin123")

        if st.button("Login", key="login_button"):
            if not username or not password:
                st.error("Please enter username and password.")
                return

            conn = get_connection()
            user = conn.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            ).fetchone()
            conn.close()

            if user:
                st.session_state.logged_in = True
                st.session_state.username = user["username"]
                st.session_state.role = user["role"]
                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    # ---------------- SIGNUP TAB ----------------
    with tab2:
        st.markdown("### Create HR Account")

        new_username = st.text_input("New Username", key="signup_username")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")

        if st.button("Sign Up", key="signup_button"):
            if not new_username or not new_password or not confirm_password:
                st.error("Please fill all fields.")
                return

            if new_password != confirm_password:
                st.error("Passwords do not match.")
                return

            if len(new_password) < 6:
                st.error("Password must be at least 6 characters long.")
                return

            conn = get_connection()

            existing_user = conn.execute(
                "SELECT * FROM users WHERE username = ?",
                (new_username,)
            ).fetchone()

            if existing_user:
                st.error("Username already exists. Please choose another username.")
                conn.close()
                return

            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (new_username, new_password, "HR")
            )
            conn.commit()
            conn.close()

            st.success("Account created successfully. Please login now.")


def logout_button():
    if "username" in st.session_state:
        st.sidebar.write(f"Logged in as: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()