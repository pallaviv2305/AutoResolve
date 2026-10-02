import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("autoreSolve.db")

def connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            team TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_complaint(name, location, description, category, priority, team, status):
    conn = connection()
    cur = conn.execute("""
        INSERT INTO complaints
        (name, location, description, category, priority, team, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, location, description, category, priority, team, status))
    complaint_id = cur.lastrowid
    conn.commit()
    conn.close()
    return complaint_id

def get_complaints():
    conn = connection()
    rows = conn.execute(
        "SELECT * FROM complaints ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]

def update_status(complaint_id, status):
    conn = connection()
    conn.execute(
        "UPDATE complaints SET status=? WHERE id=?",
        (status, complaint_id)
    )
    conn.commit()
    conn.close()

def get_stats():
    conn = connection()
    total = conn.execute("SELECT COUNT(*) FROM complaints").fetchone()[0]
    pending = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Pending'"
    ).fetchone()[0]
    progress = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='In Progress'"
    ).fetchone()[0]
    resolved = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Resolved'"
    ).fetchone()[0]
    escalated = conn.execute(
        "SELECT COUNT(*) FROM complaints WHERE status='Escalated'"
    ).fetchone()[0]
    conn.close()
    return {
        "total": total,
        "pending": pending,
        "progress": progress,
        "resolved": resolved,
        "escalated": escalated,
    }
