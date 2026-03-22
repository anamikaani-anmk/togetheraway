import os
import shutil
from config import get_db

IMAGE_FOLDER = os.path.join(os.path.dirname(__file__), "..", "static", "images")
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def save_photo(user_id, file_path):
    # Create a unique filename
    filename = os.path.basename(file_path)
    dest_path = os.path.join(IMAGE_FOLDER, filename)

    # Copy the image into app folder
    shutil.copy(file_path, dest_path)

    # Save path to DB
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO photos (user_id, file_path) VALUES (%s, %s)", (user_id, dest_path))
    conn.commit()
    cur.close()
    conn.close()

def get_photos(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT file_path FROM photos WHERE user_id = %s ORDER BY uploaded_at DESC", (user_id,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return [row[0] for row in result]
