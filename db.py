import sqlite3
import os

DB_PATH = os.environ.get("SQLITE_PATH", "analytics.db")
MAX_PREVIEW_ROWS = 10

def execute_query(sql: str):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()

    columns = [desc[0] for desc in cursor.description]
    total_count = len(rows)
    rows_preview = [list(row) for row in rows[:MAX_PREVIEW_ROWS]]
    return columns, rows_preview, total_count