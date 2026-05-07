import streamlit as st
from database.models import (
    get_candidates,
    get_jobs,
    get_candidate_by_id,
    get_job_by_id,
    add_screening_result,
    get_screening_results
)
from genai.screening import screen_candidate


def show_screening_page():
    st.header("AI Resume Screening")

    hr_username = st.session_state.username

    candidates = get_candidates(hr_username)
    jobs = get_jobs(hr_username)

    if not candidates or not jobs:
        st.warning("Add jobs and candidates first.")
        return

    candidate_map = {f"{c['id']} - {c['name']}": c["id"] for c in candidates}
    job_map = {f"{j['id']} - {j['title']}": j["id"] for j in jobs}

    selected_candidate = st.selectbox("Select Candidate", list(candidate_map.keys()))
    selected_job = st.selectbox("Select Job", list(job_map.keys()))

    candidate_id = candidate_map[selected_candidate]
    job_id = job_map[selected_job]

    if st.button("Screen Candidate"):
        candidate = get_candidate_by_id(candidate_id, hr_username)
        job = get_job_by_id(job_id, hr_username)

        if candidate is None or job is None:
            st.error("Candidate or job not found for this HR account.")
            return

        resume_text_short = candidate["resume_text"][:1500]
        job_description_short = job["description"][:700]

        with st.spinner("Screening candidate..."):
            result = screen_candidate(
                resume_text_short,
                job_description_short,
                job["required_skills"]
            )

        # Expected result format example:
        # {
        #   "score": 80,
        #   "summary": "...",
        #   "analysis": "..."
        # }

        score = result.get("score", 0)
        summary = result.get("summary", "")
        analysis = result.get("analysis", "")

        add_screening_result(
            candidate_id,
            job_id,
            score,
            summary,
            analysis,
            hr_username
        )

        st.success("Screening completed.")

        st.metric("Match Score", f"{score}%")
        st.subheader("AI Summary")
        st.write(summary)

        st.subheader("AI Match Analysis")
        st.write(analysis)

    st.subheader("Previous Screening Results")

    results = get_screening_results(hr_username)

    if not results:
        st.info("No screening results found.")
    else:
        for result in results:
            with st.expander(
                f"{result['candidate_name']} - {result['job_title']} | Score: {result['match_score']}%"
            ):
                st.write("**AI Summary:**")
                st.write(result["ai_summary"])

                st.write("**AI Match Analysis:**")
                st.write(result["ai_match_analysis"])

                st.caption(f"Created at: {result['created_at']}")