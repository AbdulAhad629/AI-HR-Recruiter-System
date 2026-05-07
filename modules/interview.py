import streamlit as st
from database.models import (
    get_candidates,
    get_jobs,
    get_candidate_by_id,
    get_job_by_id,
    add_interview_questions,
    get_interviews,
    get_existing_interview_questions
)
from genai.interview_questions import generate_interview_questions


def show_interview_page():
    st.header("AI Interview Question Generator")

    hr_username = st.session_state.username

    candidates = get_candidates(hr_username)
    jobs = get_jobs(hr_username)

    if not candidates or not jobs:
        st.warning("Add jobs and candidates first.")
        return

    candidate_map = {f"{c['id']} - {c['name']}": c["id"] for c in candidates}
    job_map = {f"{j['id']} - {j['title']}": j["id"] for j in jobs}

    selected_candidate = st.selectbox(
        "Select Candidate",
        list(candidate_map.keys())
    )

    selected_job = st.selectbox(
        "Select Job",
        list(job_map.keys())
    )

    candidate_id = candidate_map[selected_candidate]
    job_id = job_map[selected_job]

    candidate = get_candidate_by_id(candidate_id, hr_username)
    job = get_job_by_id(job_id, hr_username)

    if candidate is None or job is None:
        st.error("Candidate or job not found.")
        return

    existing_questions = get_existing_interview_questions(
        candidate_id,
        job_id,
        hr_username
    )

    if existing_questions:
        st.success("Questions already exist for this candidate and job.")
        st.text_area(
            "Saved Interview Questions",
            existing_questions,
            height=350
        )

        regenerate = st.checkbox(
            "Regenerate questions again",
            value=False
        )
    else:
        regenerate = True

    if st.button("Generate Questions"):
        if existing_questions and not regenerate:
            st.warning(
                "Questions already exist. Tick regenerate if you want new questions."
            )
            return

        # Shorter text for faster Ollama response
        resume_text_short = (candidate["resume_text"] or "")[:400]
        job_description_short = (job["description"] or "")[:200]
        required_skills_short = (job["required_skills"] or "")[:200]

        with st.spinner("Generating focused interview questions..."):
            questions = generate_interview_questions(
                resume_text_short,
                job_description_short,
                required_skills_short
            )

        add_interview_questions(
            candidate["id"],
            job["id"],
            questions,
            hr_username
        )

        st.success("Questions generated.")
        st.text_area(
            "Interview Questions",
            questions,
            height=350
        )

    st.subheader("Previous Questions")

    interviews = get_interviews(hr_username)

    if not interviews:
        st.info("No previous questions found.")
    else:
        for interview in interviews:
            with st.expander(
                f"{interview['candidate_name']} - {interview['job_title']}"
            ):
                st.write(interview["questions"])