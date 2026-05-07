from genai.ollama_client import generate_response


def analyze_job_match(resume_text, job_description, required_skills):
    prompt = f"""
You are an HR recruitment assistant.

Compare this resume with the job.

Job Description:
{job_description}

Required Skills:
{required_skills}

Resume:
{resume_text}

Return:
1. Match percentage
2. Matching skills
3. Missing skills
4. Experience relevance
5. Final recommendation
"""
    return generate_response(prompt)