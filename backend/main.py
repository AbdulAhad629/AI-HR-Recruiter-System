from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
import tempfile
import os
import json
import requests

app = FastAPI(title="AI HR Recruiter Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "phi3:latest"


def extract_pdf_text(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()


def call_ollama(prompt: str) -> str:
    response = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={
            "model": MODEL_NAME,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert HR recruiter. Return valid JSON only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2
            }
        },
        timeout=180
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=500,
            detail=f"Ollama error: {response.text}"
        )

    return response.json()["message"]["content"]


@app.get("/")
def home():
    return {
        "message": "AI HR Recruiter backend is running"
    }


@app.get("/health")
def health():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)

        return {
            "status": "ok",
            "ollama_running": response.status_code == 200,
            "model": MODEL_NAME
        }

    except Exception:
        return {
            "status": "error",
            "ollama_running": False,
            "message": "Ollama is not reachable"
        }


@app.post("/analyze")
async def analyze_candidate(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    if not resume.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(await resume.read())
        temp_path = temp_file.name

    try:
        resume_text = extract_pdf_text(temp_path)

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from resume PDF."
            )

        prompt = f"""
Analyze the candidate resume against the job description.

Return valid JSON only using this structure:

{{
  "candidate_score": 0,
  "fit_level": "",
  "matched_skills": [],
  "missing_skills": [],
  "strengths": [],
  "weaknesses": [],
  "summary": "",
  "interview_questions": [],
  "hiring_recommendation": ""
}}

Scoring rules:
- 90-100: Excellent fit
- 75-89: Strong fit
- 60-74: Moderate fit
- 40-59: Weak fit
- 0-39: Poor fit

Job Description:
{job_description}

Candidate Resume:
{resume_text}
"""

        result_text = call_ollama(prompt)

        try:
            result_json = json.loads(result_text)
        except json.JSONDecodeError:
            result_json = {
                "raw_response": result_text
            }

        return {
            "success": True,
            "model": MODEL_NAME,
            "result": result_json
        }

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)