from config import get_db
import random

def get_random_prompt():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("SELECT text FROM prompts")
        prompts = cur.fetchall()

        if not prompts:
            return "💌 Write something kind to your partner today."

        return random.choice(prompts)[0]
    finally:
        cur.close()
        conn.close()
