import streamlit as st
from database.models import get_candidates


def show_candidates_page():
    st.header("Candidates")

    candidates = get_candidates(st.session_state.username)

    if not candidates:
        st.info("No candidates uploaded yet.")
        return

    for candidate in candidates:
        with st.expander(f"{candidate['id']} - {candidate['name']}"):
            st.write(f"**Email:** {candidate['email']}")
            st.write(f"**Phone:** {candidate['phone']}")
            st.write(f"**Resume Path:** {candidate['resume_path']}")
            st.write(f"**Uploaded At:** {candidate['created_at']}")

            st.subheader("Resume Text")
            st.text_area(
                "Extracted Resume Text",
                candidate["resume_text"],
                height=250,
                key=f"resume_text_{candidate['id']}"
            )