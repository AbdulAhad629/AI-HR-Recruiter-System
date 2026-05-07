from genai.ollama_client import generate_response


def summarize_resume(resume_text):
    prompt = f"""
You are an HR assistant.

Summarize this resume.

Include:
1. Candidate profile
2. Skills
3. Education
4. Experience
5. Strengths
6. Weaknesses

Resume:
{resume_text}
"""
    return generate_response(prompt)