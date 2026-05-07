import streamlit as st
from database.models import (
    get_jobs,
    get_candidates,
    get_screening_results,
    get_interviews
)


def show_dashboard_page():
    st.header("Dashboard")

    hr_username = st.session_state.username

    jobs = get_jobs(hr_username)
    candidates = get_candidates(hr_username)
    screenings = get_screening_results(hr_username)
    interviews = get_interviews(hr_username)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Jobs", len(jobs))
    col2.metric("Candidates", len(candidates))
    col3.metric("Screenings", len(screenings))
    col4.metric("Interviews", len(interviews))

    st.subheader("Recent Jobs")
    if jobs:
        for job in jobs[:5]:
            st.write(f"**{job['title']}** — {job['department']}")
    else:
        st.info("No jobs added yet.")

    st.subheader("Recent Candidates")
    if candidates:
        for candidate in candidates[:5]:
            st.write(f"**{candidate['name']}** — {candidate['email']}")
    else:
        st.info("No candidates uploaded yet.")