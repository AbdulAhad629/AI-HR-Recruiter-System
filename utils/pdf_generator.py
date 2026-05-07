from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from pathlib import Path


def generate_candidate_report(name, job_title, score, summary, analysis, questions):
    file_path = Path(f"report_{name.replace(' ', '_')}.pdf")

    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    # Title
    elements.append(Paragraph("AI Recruitment Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Candidate Info
    elements.append(Paragraph(f"<b>Candidate:</b> {name}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Job Role:</b> {job_title}", styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Score Section
    elements.append(Paragraph(f"<b>Match Score:</b> {score}/100", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    # Score Table
    score_table = [
        ["Category", "Score"],
        ["Overall Match", f"{score}/100"]
    ]

    table = Table(score_table)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Summary
    elements.append(Paragraph("<b>AI Resume Summary</b>", styles["Heading3"]))
    elements.append(Paragraph(summary, styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Analysis
    elements.append(Paragraph("<b>AI Match Analysis</b>", styles["Heading3"]))
    elements.append(Paragraph(analysis, styles["Normal"]))
    elements.append(Spacer(1, 10))

    # Questions
    elements.append(Paragraph("<b>Interview Questions</b>", styles["Heading3"]))
    elements.append(Paragraph(questions.replace("\n", "<br/>"), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Footer
    elements.append(Paragraph(
        "<i>Note: This report is AI-generated and should be used for decision support only.</i>",
        styles["Normal"]
    ))

    doc.build(elements)

    return file_path