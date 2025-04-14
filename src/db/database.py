import sqlite3
from datetime import datetime

DB_FILE = "astrology_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            question TEXT,
            interpretation TEXT,
            datetime TEXT,
            location TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_question(user_id, question, interpretation, datetime_data, location_data):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_questions (user_id, question, interpretation, datetime, location, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        question,
        interpretation,
        str(datetime_data),
        str(location_data),
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()

def get_last_n_questions(user_id, n=3):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT question, interpretation FROM user_questions
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, n))
    rows = cursor.fetchall()
    conn.close()
    return [{"question": r[0], "interpretation": r[1]} for r in rows]
