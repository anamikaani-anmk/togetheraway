from config import get_db
conn = get_db()
cur = conn.cursor()
cur.execute("SELECT * FROM partners")
print(cur.fetchall())
conn.close()
