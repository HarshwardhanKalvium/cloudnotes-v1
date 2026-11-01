import sqlite3
import os

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    filename TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "png", "jpg", "jpeg", "gif"}


def get_db_connection(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_connection(db_path)
    with conn:
        conn.executescript(SCHEMA)
    conn.close()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
