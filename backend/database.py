import sqlite3
from datetime import datetime

DB_PATH = "conversations.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            thread_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def create_conversation(thread_id, title):
    conn = get_connection()

    now = datetime.now().isoformat()

    conn.execute("""
        INSERT INTO conversations
        (thread_id, title, created_at, updated_at)
        VALUES (?, ?, ?, ?)
    """, (thread_id, title, now, now))

    conn.commit()
    conn.close()

def conversation_exists(thread_id):
    conn = get_connection()

    result = conn.execute(
        "SELECT 1 FROM conversations WHERE thread_id = ?",
        (thread_id,)
    ).fetchone()

    conn.close()

    return result is not None    


def get_conversations():
    conn = get_connection()

    rows = conn.execute("""
        SELECT thread_id, title, created_at, updated_at
        FROM conversations
        ORDER BY updated_at DESC
    """).fetchall()

    conn.close()

    return [
        {
            "thread_id": row[0],
            "title": row[1],
            "created_at": row[2],
            "updated_at": row[3]
        }
        for row in rows
    ]

def update_conversation_title(thread_id, title):
    conn = get_connection()

    conn.execute("""
        UPDATE conversations
        SET title = ?, updated_at = ?
        WHERE thread_id = ?
    """, (title, datetime.now().isoformat(), thread_id))

    conn.commit()
    conn.close()