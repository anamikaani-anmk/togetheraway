# file: plot_mood.py

from config import get_db
import matplotlib.pyplot as plt

def plot_mood(user_id, days=14):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT mood_date, AVG(rating)
            FROM moods
            WHERE user_id=%s
            GROUP BY mood_date
            ORDER BY mood_date ASC
            LIMIT %s
        """, (user_id, days))

        rows = cur.fetchall()

        if not rows:
            print("No mood data to plot yet.")
            return

        dates = [row[0] for row in rows]
        ratings = [float(row[1]) for row in rows]

        plt.figure(figsize=(8, 4))
        plt.plot(dates, ratings, marker='o', linewidth=2, linestyle='solid')
        plt.title("💗 Mood Trend Over Time")
        plt.xlabel("Date")
        plt.ylabel("Mood Rating (1–10)")
        plt.ylim(1, 10)
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    finally:
        cur.close()
        conn.close()
