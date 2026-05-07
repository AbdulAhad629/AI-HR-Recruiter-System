from genai.ollama_client import generate_response
import re


def clean_words(text):
    text = (text or "").lower()
    return re.findall(r"[a-zA-Z0-9+#.]+", text)


def calculate_keyword_score(resume_text, required_skills):
    resume_words = set(clean_words(resume_text))

    skills = [
        skill.strip().lower()
        for skill in required_skills.replace("\n", ",").split(",")
        if skill.strip()
    ]

    if not skills:
        return 0, [], []

    matched = []
    missing = []

    for skill in skills:
        skill_words = clean_words(skill)

        if any(word in resume_words for word in skill_words):
            matched.append(skill)
        else:
            missing.append(skill)

    score = int((len(matched) / len(skills)) * 100)
    return score, matched, missing


def screen_candidate(resume_text, job_description, required_skills):
    score, matched, missing = calculate_keyword_score(resume_text, required_skills)

    prompt = f"""
Write a short HR screening explanation.

Match Score: {score}
Matched Skills: {", ".join(matched)}
Missing Skills: {", ".join(missing)}

Return only:
Summary: <one line>
Recommendation: <Shortlist/Hold/Reject>
"""

    ai_response = generate_response(prompt)

    analysis = f"""
Match Score: {score}

Matched Skills:
{", ".join(matched) if matched else "None"}

Missing Skills:
{", ".join(missing) if missing else "None"}

AI Explanation:
{ai_response}
"""

    return {
        "score": score,
        "summary": "Screening completed using skill matching and GenAI explanation.",
        "analysis": analysis
    }