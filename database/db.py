import sqlite3
from pathlib import Path
from config.settings import DATABASE_PATH


def get_connection():
    Path("data").mkdir(exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def add_column_if_not_exists(cur, table_name, column_name, column_type):
    """
    SQLite does not automatically update old tables when we change CREATE TABLE.
    This function safely adds a column if it does not already exist.
    """
    cur.execute(f"PRAGMA table_info({table_name})")
    columns = [column["name"] for column in cur.fetchall()]

    if column_name not in columns:
        cur.execute(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # ---------------- USERS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # ---------------- JOBS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        department TEXT,
        description TEXT,
        required_skills TEXT,
        experience_required TEXT,
        hr_username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- CANDIDATES TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        resume_path TEXT,
        resume_text TEXT,
        hr_username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- SCREENING RESULTS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS screening_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        job_id INTEGER,
        match_score INTEGER,
        ai_summary TEXT,
        ai_match_analysis TEXT,
        hr_username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- INTERVIEWS TABLE ----------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER,
        job_id INTEGER,
        questions TEXT,
        hr_username TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # ---------------- MIGRATION FOR OLD DATABASE ----------------
    # If these tables already existed before hr_username was added,
    # this will add the missing column safely.
    add_column_if_not_exists(cur, "jobs", "hr_username", "TEXT")
    add_column_if_not_exists(cur, "candidates", "hr_username", "TEXT")
    add_column_if_not_exists(cur, "screening_results", "hr_username", "TEXT")
    add_column_if_not_exists(cur, "interviews", "hr_username", "TEXT")

    # ---------------- DEFAULT ADMIN ACCOUNT ----------------
    cur.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            ("admin", "admin123", "HR Admin")
        )

    # ---------------- ASSIGN OLD RECORDS TO ADMIN ----------------
    # Old records created before multi-user support may have NULL hr_username.
    # Assigning them to admin prevents them from disappearing after filtering.
    cur.execute("""
        UPDATE jobs
        SET hr_username = 'admin'
        WHERE hr_username IS NULL
    """)

    cur.execute("""
        UPDATE candidates
        SET hr_username = 'admin'
        WHERE hr_username IS NULL
    """)

    cur.execute("""
        UPDATE screening_results
        SET hr_username = 'admin'
        WHERE hr_username IS NULL
    """)

    cur.execute("""
        UPDATE interviews
        SET hr_username = 'admin'
        WHERE hr_username IS NULL
    """)

    conn.commit()
    conn.close()