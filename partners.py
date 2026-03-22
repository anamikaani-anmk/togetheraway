from config import get_db
def request_partner(requester_id, partner_username):
    conn = get_db()
    cur = conn.cursor()
    try:
        # find the partner user_id
        cur.execute("SELECT user_id FROM users WHERE username=%s", (partner_username,))
        result = cur.fetchone()

        if not result:
            print("⚠ Partner username not found.")
            return
        
        partner_id = result[0]
        # create partner request entry
        cur.execute(
            "INSERT INTO partners (user_a, user_b, status) VALUES (%s, %s, 'requested')",
            (requester_id, partner_id)
        )
        conn.commit()
        print("💌 Partner request sent!")
    except Exception as e:
        print("❌ Error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
def accept_partner(pair_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE partners SET status='connected' WHERE pair_id=%s", (pair_id,))
        conn.commit()
        print("💞 Partner request accepted! You are now connected.")
    except Exception as e:
        print("❌ Error:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
