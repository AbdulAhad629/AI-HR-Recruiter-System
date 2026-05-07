import re


def find_matched_skills(resume_text, required_skills):
    resume_text = (resume_text or "").lower()
    skills = [s.strip().lower() for s in (required_skills or "").split(",") if s.strip()]

    matched = []
    missing = []

    for skill in skills:
        if re.search(r"\b" + re.escape(skill) + r"\b", resume_text):
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing


def extract_years_experience(text):
    text = (text or "").lower()
    patterns = [
        r"(\d+)\+?\s+years",
        r"(\d+)\+?\s+year",
        r"(\d+)\+?\s+yrs",
        r"(\d+)\+?\s+yr"
    ]

    years = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        years.extend([int(x) for x in found])

    return max(years) if years else 0


def calculate_candidate_score(resume_text, job_title, required_skills, experience_required):
    matched_skills, missing_skills = find_matched_skills(resume_text, required_skills)

    total_skills = len([s for s in (required_skills or "").split(",") if s.strip()])
    skill_ratio = len(matched_skills) / total_skills if total_skills else 0
    skill_score = skill_ratio * 40

    resume_years = extract_years_experience(resume_text)
    required_years = extract_years_experience(experience_required)

    if required_years == 0:
        experience_score = 15
    else:
        experience_score = min(resume_years / required_years, 1) * 25

    education_keywords = "bs, bsc, bachelor, bachelors, ms, msc, master, degree, university"
    education_found, _ = find_matched_skills(resume_text, education_keywords)
    education_score = min((len(education_found) / 4) * 15, 15)

    role_keywords = ", ".join((job_title or "").split())
    role_found, _ = find_matched_skills(resume_text, role_keywords)
    role_score = min(len(role_found) * 5, 10)

    word_count = len((resume_text or "").split())

    if word_count >= 250:
        quality_score = 10
    elif word_count >= 150:
        quality_score = 7
    elif word_count >= 80:
        quality_score = 4
    else:
        quality_score = 2

    final_score = skill_score + experience_score + education_score + role_score + quality_score
    final_score = round(min(final_score, 95), 2)

    breakdown = {
        "Skills Match": round(skill_score, 2),
        "Experience": round(experience_score, 2),
        "Education": round(education_score, 2),
        "Role Match": round(role_score, 2),
        "Resume Quality": round(quality_score, 2),
        "Matched Skills": matched_skills,
        "Missing Skills": missing_skills,
        "Resume Experience Years": resume_years,
        "Required Experience Years": required_years
    }

    return final_score, breakdown


def score_label(score):
    if score >= 85:
        return "Excellent Match"
    elif score >= 70:
        return "Strong Match"
    elif score >= 55:
        return "Moderate Match"
    elif score >= 40:
        return "Weak Match"
    else:
        return "Not Recommended"