import streamlit as st
from database.models import add_job, get_jobs


def show_jobs_page():
    st.header("Job Management")

    hr_username = st.session_state.username

    with st.form("add_job_form"):
        title = st.text_input("Job Title")
        department = st.text_input("Department")
        description = st.text_area("Job Description")
        required_skills = st.text_area("Required Skills")
        experience_required = st.text_input("Experience Required")

        submitted = st.form_submit_button("Add Job")

        if submitted:
            if not title or not description or not required_skills:
                st.error("Please fill Job Title, Description, and Required Skills.")
            else:
                add_job(
                    title,
                    department,
                    description,
                    required_skills,
                    experience_required,
                    hr_username
                )
                st.success("Job added successfully.")
                st.rerun()

    st.subheader("Your Jobs")

    jobs = get_jobs(hr_username)

    if not jobs:
        st.info("No jobs added yet.")
    else:
        for job in jobs:
            with st.expander(f"{job['title']} - {job['department']}"):
                st.write("**Description:**")
                st.write(job["description"])

                st.write("**Required Skills:**")
                st.write(job["required_skills"])

                st.write("**Experience Required:**")
                st.write(job["experience_required"])

                st.caption(f"Created at: {job['created_at']}")