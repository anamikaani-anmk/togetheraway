from config import get_db
import datetime
def log_mood(user_id, mood_tag, rating, note=""):
    conn = get_db()
    cur = conn.cursor()
    today = datetime.date.today()
    try:
        cur.execute(
            "INSERT INTO moods (user_id, mood_tag, rating, mood_note, mood_date) VALUES (%s, %s, %s, %s, %s)",
            (user_id, mood_tag, rating, note, today)
        )
        conn.commit()
        print("📝 Mood logged for today!")
    except Exception as e:
        print("❌ Error logging mood:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def view_moods(user_id, limit=10):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "SELECT mood_date, mood_tag, rating, mood_note FROM moods WHERE user_id=%s ORDER BY mood_date DESC LIMIT %s",
            (user_id, limit)
        )
        rows = cur.fetchall()
        if rows:
            for r in rows:
                print(f"{r['mood_date']} → {r['mood_tag']} ({r['rating']}/10) — {r['mood_note']}")
        else:
            print("🫧 No moods logged yet.")
    finally:
        cur.close()
        conn.close()
def compare_partner_mood(pair_id, date):
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    try:
        # find the two users in the pair
        cur.execute("SELECT user_a, user_b FROM partners WHERE pair_id=%s AND status='connected'", (pair_id,))
        pair = cur.fetchone()

        if not pair:
            print("💔 No connected partner found.")
            return

        user1 = pair["user_a"]
        user2 = pair["user_b"]

        # fetch moods of both on given date
        cur.execute("""
            SELECT user_id, mood_tag, rating, mood_note
            FROM moods
            WHERE mood_date=%s AND user_id IN (%s, %s)
        """, (date, user1, user2))

        rows = cur.fetchall()

        if not rows:
            print("☁ No moods logged that day.")
            return

        print(f"💞 Mood Comparison for {date}:")
        for r in rows:
            name = "Partner 1" if r["user_id"] == user1 else "Partner 2"
            print(f"{name} → {r['mood_tag']} ({r['rating']}/10) — {r['mood_note']}")
    finally:
        cur.close()
        conn.close()
def get_moods_by_date(pair_id, date):
    conn = get_db()
    cur = conn.cursor(dictionary=True)

    # get the 2 users linked to the pair
    cur.execute("SELECT user_a, user_b FROM partners WHERE pair_id=%s", (pair_id,))
    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return None

    u1, u2 = row["user_a"], row["user_b"]

    cur.execute("""
        SELECT user_id, mood_tag, rating, mood_note
        FROM moods
        WHERE mood_date=%s AND user_id IN (%s, %s)
    """, (date, u1, u2))

    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


