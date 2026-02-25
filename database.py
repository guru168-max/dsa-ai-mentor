import sqlite3

conn = sqlite3.connect("dsa_history.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    thread_id TEXT,
    role TEXT,
    content TEXT
)
""")
conn.commit()

def save_message(thread_id, role, content):
    cursor.execute(
        "INSERT INTO messages (thread_id, role, content) VALUES (?, ?, ?)",
        (thread_id, role, content),
    )
    conn.commit()

def load_messages(thread_id):
    cursor.execute(
        "SELECT role, content FROM messages WHERE thread_id=?",
        (thread_id,),
    )
    return cursor.fetchall()
