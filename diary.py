from config import get_db
from datetime import datetime

# PRIVATE DIARY
def add_private_entry(user_id, content):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO diary_private (user_id, content) VALUES (%s, %s)",
        (user_id, content)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_private_entries(user_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT content, created_at FROM diary_private WHERE user_id=%s ORDER BY created_at DESC",
        (user_id,)
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# SHARED DIARY
def add_shared_entry(pair_id, user_id, content):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO diary_shared (pair_id, writer_id, content) VALUES (%s, %s, %s)",
        (pair_id, user_id, content)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_shared_entries(pair_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT diary_shared.content, diary_shared.created_at, users.username
        FROM diary_shared
        JOIN users ON diary_shared.writer_id = users.user_id
        WHERE diary_shared.pair_id=%s
        ORDER BY diary_shared.created_at DESC
    """, (pair_id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data
