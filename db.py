import sqlite3
from pathlib import Path

DB_PATH = Path.home() / ".local/share/shellmemo/shellmemo.db"

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            description TEXT,
            tags TEXT,
            sort_order INTEGER
        )
        """)

def add_entry(content, description="", tags=""):
    with sqlite3.connect(DB_PATH) as conn:
        max_order = conn.execute("SELECT MAX(sort_order) FROM entries").fetchone()[0]
        next_order = (max_order or 0) + 1

        conn.execute(
            "INSERT INTO entries (content, description, tags, sort_order) VALUES (?, ?, ?, ?)",
            (content, description, tags, next_order)
        )

def update_entry(entry_id, content, description, tags):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "UPDATE entries SET content=?, description=?, tags=? WHERE id=?",
            (content, description, tags, entry_id)
        )

def delete_entry(entry_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM entries WHERE id=?", (entry_id,))

def get_entries():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute("""
        SELECT id, content, description, tags, sort_order
        FROM entries
        ORDER BY sort_order ASC
        """).fetchall()

# 🔥 並び順一括更新
def update_order_bulk(id_list):
    with sqlite3.connect(DB_PATH) as conn:
        for idx, entry_id in enumerate(id_list):
            conn.execute(
                "UPDATE entries SET sort_order=? WHERE id=?",
                (idx, entry_id)
            )
