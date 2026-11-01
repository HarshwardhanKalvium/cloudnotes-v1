import os

import psycopg2
from psycopg2.extras import RealDictCursor

MIGRATION = """
CREATE TABLE IF NOT EXISTS notes (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    filename TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

ALLOWED_EXTENSIONS = {"txt", "md", "pdf", "png", "jpg", "jpeg", "gif"}


def get_db_connection(database_url):
    return psycopg2.connect(database_url, cursor_factory=RealDictCursor)


def init_db(database_url):
    conn = get_db_connection(database_url)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(MIGRATION)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
