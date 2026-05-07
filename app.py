import streamlit as st
from database.db import init_db
from auth.login import login_form, logout_button
from modules.dashboard import show_dashboard_page
from modules.jobs import show_jobs_page
from modules.resume_upload import show_resume_upload_page
from modules.candidates import show_candidates_page
from modules.screening import show_screening_page
from modules.interview import show_interview_page
from modules.reports import show_reports_page


st.set_page_config(
    page_title="The IntelliHire Management System",
    page_icon="🧑‍💼",
    layout="wide"
)

# Initialize database
init_db()

# Initialize session variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "role" not in st.session_state:
    st.session_state.role = ""

# App title
st.title("🧑‍💼 The IntelliHire Management System")
st.caption("Free GenAI version using Ollama local LLM")

# Authentication check
if not st.session_state.logged_in:
    login_form()
    st.stop()

# Sidebar logout
logout_button()

st.sidebar.markdown("---")
st.sidebar.success(f"Welcome, {st.session_state.username}")

# Navigation
page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Jobs",
        "Upload Resume",
        "Candidates",
        "Screening",
        "Interview",
        "Reports"
    ]
)

# Page routing
if page == "Dashboard":
    show_dashboard_page()

elif page == "Jobs":
    show_jobs_page()

elif page == "Upload Resume":
    show_resume_upload_page()

elif page == "Candidates":
    show_candidates_page()

elif page == "Screening":
    show_screening_page()

elif page == "Interview":
    show_interview_page()

elif page == "Reports":
    show_reports_page()