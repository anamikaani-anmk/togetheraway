from config import get_db
conn = get_db()
if conn:
    print("Connection successful!")
    conn.close()
