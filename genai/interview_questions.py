from genai.ollama_client import generate_response
import re


def extract_skills_from_text(text, required_skills):
    text = (text or "").lower()

    skills = [
        skill.strip()
        for skill in required_skills.replace("\n", ",").split(",")
        if skill.strip()
    ]

    matched = []
    missing = []

    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in text:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


def generate_interview_questions(resume_text, job_description, required_skills):
    resume_text = (resume_text or "")[:400]
    job_description = (job_description or "")[:200]
    required_skills = (required_skills or "")[:200]

    matched_skills, missing_skills = extract_skills_from_text(
        resume_text,
        required_skills
    )

    prompt = f"""
Generate exactly 6 short interview questions.

Required Skills:
{required_skills}

Matched Skills:
{", ".join(matched_skills)}

Missing Skills:
{", ".join(missing_skills)}

Job:
{job_description}

Rules:
- 3 technical questions
- 2 HR questions
- 1 scenario question
- No answers
- No explanation
- Each question under 15 words

Format:
Technical:
1.
2.
3.

HR:
1.
2.

Scenario:
1.
"""

    return generate_response(prompt)