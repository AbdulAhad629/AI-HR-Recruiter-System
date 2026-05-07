from database.db import get_connection


# ---------------- JOBS ----------------

def add_job(title, department, description, required_skills, experience_required, hr_username):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO jobs 
        (title, department, description, required_skills, experience_required, hr_username) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, department, description, required_skills, experience_required, hr_username)
    )
    conn.commit()
    conn.close()


def get_jobs(hr_username):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM jobs 
        WHERE hr_username = ?
        ORDER BY id DESC
        """,
        (hr_username,)
    ).fetchall()
    conn.close()
    return rows


def get_job_by_id(job_id, hr_username):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT * FROM jobs 
        WHERE id = ? AND hr_username = ?
        """,
        (job_id, hr_username)
    ).fetchone()
    conn.close()
    return row


# ---------------- CANDIDATES ----------------

def add_candidate(name, email, phone, resume_path, resume_text, hr_username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO candidates 
        (name, email, phone, resume_path, resume_text, hr_username) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, email, phone, resume_path, resume_text, hr_username)
    )
    candidate_id = cur.lastrowid
    conn.commit()
    conn.close()
    return candidate_id


def get_candidates(hr_username):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT * FROM candidates 
        WHERE hr_username = ?
        ORDER BY id DESC
        """,
        (hr_username,)
    ).fetchall()
    conn.close()
    return rows


def get_candidate_by_id(candidate_id, hr_username):
    conn = get_connection()
    row = conn.execute(
        """
        SELECT * FROM candidates 
        WHERE id = ? AND hr_username = ?
        """,
        (candidate_id, hr_username)
    ).fetchone()
    conn.close()
    return row


# ---------------- SCREENING RESULTS ----------------

def add_screening_result(candidate_id, job_id, score, summary, analysis, hr_username):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO screening_results 
        (candidate_id, job_id, match_score, ai_summary, ai_match_analysis, hr_username) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (candidate_id, job_id, score, summary, analysis, hr_username)
    )
    conn.commit()
    conn.close()


def get_screening_results(hr_username):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT 
            sr.id,
            sr.candidate_id,
            sr.job_id,
            c.name AS candidate_name,
            j.title AS job_title,
            sr.match_score,
            sr.ai_summary,
            sr.ai_match_analysis,
            sr.created_at
        FROM screening_results sr
        JOIN candidates c ON sr.candidate_id = c.id
        JOIN jobs j ON sr.job_id = j.id
        WHERE sr.hr_username = ?
        ORDER BY sr.match_score DESC
        """,
        (hr_username,)
    ).fetchall()
    conn.close()
    return rows


def get_existing_screening_result(candidate_id, job_id, hr_username):
    """
    Check if this candidate has already been screened
    for this job by the same HR user.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT *
        FROM screening_results
        WHERE candidate_id = ? AND job_id = ? AND hr_username = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (candidate_id, job_id, hr_username)
    ).fetchone()
    conn.close()
    return row


# ---------------- INTERVIEWS ----------------

def add_interview_questions(candidate_id, job_id, questions, hr_username):
    conn = get_connection()
    conn.execute(
        """
        INSERT INTO interviews 
        (candidate_id, job_id, questions, hr_username) 
        VALUES (?, ?, ?, ?)
        """,
        (candidate_id, job_id, questions, hr_username)
    )
    conn.commit()
    conn.close()


def get_interviews(hr_username):
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT 
            interviews.id,
            interviews.candidate_id,
            interviews.job_id,
            candidates.name AS candidate_name,
            jobs.title AS job_title,
            interviews.questions,
            interviews.created_at
        FROM interviews
        JOIN candidates ON interviews.candidate_id = candidates.id
        JOIN jobs ON interviews.job_id = jobs.id
        WHERE interviews.hr_username = ?
        ORDER BY interviews.id DESC
        """,
        (hr_username,)
    ).fetchall()
    conn.close()
    return rows


def get_existing_interview_questions(candidate_id, job_id, hr_username):
    """
    Check if interview questions already exist
    for this candidate and job by the same HR user.
    """
    conn = get_connection()
    row = conn.execute(
        """
        SELECT questions 
        FROM interviews
        WHERE candidate_id = ? AND job_id = ? AND hr_username = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (candidate_id, job_id, hr_username)
    ).fetchone()
    conn.close()

    if row:
        return row["questions"]

    return None