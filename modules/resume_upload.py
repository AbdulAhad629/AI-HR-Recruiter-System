import streamlit as st
from pathlib import Path

from database.models import add_candidate
from utils.resume_parser import extract_resume_text


def show_resume_upload_page():
    st.header("Upload Candidate Resume")

    name = st.text_input("Candidate Name")
    email = st.text_input("Candidate Email")
    phone = st.text_input("Candidate Phone")

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    if st.button("Upload Resume"):
        if not name or not email or not uploaded_file:
            st.error("Please enter candidate name, email, and upload resume.")
            return

        upload_dir = Path("data/resumes")
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / uploaded_file.name

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        resume_text = extract_resume_text(str(file_path))

        candidate_id = add_candidate(
            name,
            email,
            phone,
            str(file_path),
            resume_text,
            st.session_state.username
        )

        st.success(f"Candidate uploaded successfully. Candidate ID: {candidate_id}")