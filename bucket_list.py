from config import get_db

def add_bucket_item(pair_id, title, description=""):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO bucket_list (pair_id, title, description)
        VALUES (%s, %s, %s)
    """, (pair_id, title, description))
    conn.commit()
    cur.close()
    conn.close()


def get_bucket_items(pair_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT item_id, title, description
        FROM bucket_list
        WHERE pair_id=%s AND completed=0
        ORDER BY created_at DESC
    """, (pair_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items


def get_done_items(pair_id):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    cur.execute("""
        SELECT item_id, title, description
        FROM bucket_list
        WHERE pair_id=%s AND completed=1
        ORDER BY created_at DESC
    """, (pair_id,))
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items


def complete_item(item_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE bucket_list
        SET completed=1
        WHERE item_id=%s
    """, (item_id,))
    conn.commit()
    cur.close()
    conn.close()
