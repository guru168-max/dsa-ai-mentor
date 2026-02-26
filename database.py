import sqlite3
from datetime import datetime

conn = sqlite3.connect("dsa_ai.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- USERS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ---------------- SUBMISSIONS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS submissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    topic TEXT,
    difficulty TEXT,
    problem TEXT,
    code TEXT,
    result TEXT,
    is_correct INTEGER,
    timestamp TEXT
)
""")

# ---------------- DAILY TASKS TABLE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    topic TEXT,
    pattern TEXT,
    intuition TEXT,
    completed INTEGER DEFAULT 0,
    date TEXT DEFAULT CURRENT_DATE
)
""")

conn.commit()

# ---------------- CREATE USER ----------------
def create_user(username, password):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False

# ---------------- AUTHENTICATE USER ----------------
def authenticate_user(username, password):
    cursor.execute(
        "SELECT id, username FROM users WHERE username=? AND password=?",
        (username, password)
    )
    return cursor.fetchone()

# ---------------- SAVE SUBMISSION ----------------
def save_submission(user_id, topic, difficulty, mode,
                    problem, code, result, is_correct):

    cursor.execute("""
        INSERT INTO submissions
        (user_id, topic, difficulty, problem, code,
         result, is_correct, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        topic,
        difficulty,
        problem,
        code,
        result,
        is_correct,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
