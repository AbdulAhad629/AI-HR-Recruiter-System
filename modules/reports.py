import streamlit as st
import pandas as pd
from io import BytesIO
from fpdf import FPDF

from database.models import (
    get_candidates,
    get_jobs,
    get_screening_results,
    get_interviews
)


def clean_text(text):
    """
    FPDF has issues with some special characters.
    This makes text safe for PDF.
    """
    if text is None:
        return ""

    return str(text).encode("latin-1", "replace").decode("latin-1")


def create_pdf_report(candidates, jobs, screening_results, interviews, hr_username):
    """
    Creates a PDF report and returns it as bytes.
    """
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "IntelliHire HR Report", ln=True, align="C")

    pdf.ln(5)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Generated For: {clean_text(hr_username)}", ln=True)

    pdf.ln(5)

    # Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Summary", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Total Candidates: {len(candidates)}", ln=True)
    pdf.cell(0, 8, f"Total Jobs: {len(jobs)}", ln=True)
    pdf.cell(0, 8, f"Screening Results: {len(screening_results)}", ln=True)
    pdf.cell(0, 8, f"Interview Questions: {len(interviews)}", ln=True)

    pdf.ln(5)

    # Screening Results
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Screening Results", ln=True)

    if not screening_results:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, "No screening results found.", ln=True)
    else:
        for result in screening_results:
            pdf.set_font("Arial", "B", 11)
            title = f"{result['candidate_name']} - {result['job_title']} | Score: {result['match_score']}%"
            pdf.multi_cell(0, 8, clean_text(title))

            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 7, clean_text(f"AI Summary: {result['ai_summary']}"))
            pdf.multi_cell(0, 7, clean_text(f"AI Match Analysis: {result['ai_match_analysis']}"))
            pdf.multi_cell(0, 7, clean_text(f"Created At: {result['created_at']}"))

            pdf.ln(3)

    pdf.ln(5)

    # Interview Questions
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Interview Questions", ln=True)

    if not interviews:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 8, "No interview questions found.", ln=True)
    else:
        for interview in interviews:
            pdf.set_font("Arial", "B", 11)
            title = f"{interview['candidate_name']} - {interview['job_title']}"
            pdf.multi_cell(0, 8, clean_text(title))

            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 7, clean_text(interview["questions"]))

            if "created_at" in interview.keys():
                pdf.multi_cell(0, 7, clean_text(f"Created At: {interview['created_at']}"))

            pdf.ln(3)

    pdf_output = pdf.output(dest="S").encode("latin-1")
    return pdf_output


def create_screening_csv(screening_results):
    """
    Creates CSV bytes for screening results.
    """
    data = []

    for result in screening_results:
        data.append({
            "Candidate": result["candidate_name"],
            "Job": result["job_title"],
            "Match Score": result["match_score"],
            "AI Summary": result["ai_summary"],
            "AI Match Analysis": result["ai_match_analysis"],
            "Created At": result["created_at"]
        })

    df = pd.DataFrame(data)

    if df.empty:
        df = pd.DataFrame(columns=[
            "Candidate",
            "Job",
            "Match Score",
            "AI Summary",
            "AI Match Analysis",
            "Created At"
        ])

    return df.to_csv(index=False).encode("utf-8")


def show_reports_page():
    st.header("Reports")

    # Small safety improvement
    if "username" not in st.session_state or not st.session_state.username:
        st.error("Please login first.")
        return

    hr_username = st.session_state.username

    candidates = get_candidates(hr_username)
    jobs = get_jobs(hr_username)
    screening_results = get_screening_results(hr_username)
    interviews = get_interviews(hr_username)

    st.subheader("Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Candidates", len(candidates))
    col2.metric("Total Jobs", len(jobs))
    col3.metric("Screening Results", len(screening_results))
    col4.metric("Interview Questions", len(interviews))

    st.divider()

    # Download buttons
    st.subheader("Download Reports")

    pdf_report = create_pdf_report(
        candidates,
        jobs,
        screening_results,
        interviews,
        hr_username
    )

    st.download_button(
        label="Download Full PDF Report",
        data=pdf_report,
        file_name="intellihire_hr_report.pdf",
        mime="application/pdf"
    )

    csv_report = create_screening_csv(screening_results)

    st.download_button(
        label="Download Screening CSV Report",
        data=csv_report,
        file_name="screening_results.csv",
        mime="text/csv"
    )

    st.divider()

    st.subheader("Screening Results")

    if not screening_results:
        st.info("No screening results found.")
    else:
        for result in screening_results:
            with st.expander(
                f"{result['candidate_name']} - {result['job_title']} | Score: {result['match_score']}%"
            ):
                st.write("**AI Summary:**")
                st.write(result["ai_summary"])

                st.write("**AI Match Analysis:**")
                st.write(result["ai_match_analysis"])

                st.caption(f"Created at: {result['created_at']}")

    st.divider()

    st.subheader("Interview Questions")

    if not interviews:
        st.info("No interview questions found.")
    else:
        for interview in interviews:
            with st.expander(
                f"{interview['candidate_name']} - {interview['job_title']}"
            ):
                st.write(interview["questions"])

                if "created_at" in interview.keys():
                    st.caption(f"Created at: {interview['created_at']}")