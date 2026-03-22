from config import get_db

def register(username, password):
    conn = get_db()
    cur = conn.cursor()

    # Check if username exists
    cur.execute("SELECT user_id FROM users WHERE username = %s", (username,))
    existing = cur.fetchone()

    if existing:
        cur.close()
        conn.close()
        return False  # username already exists

    # Insert new user
    cur.execute("""
        INSERT INTO users (username, password_hash)
        VALUES (%s, %s)
    """, (username, password))

    conn.commit()
    cur.close()
    conn.close()
    return True


def login(username, password):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT user_id FROM users
        WHERE username = %s AND password_hash = %s
    """, (username, password))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else None


def get_pair_id(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT pair_id FROM partners
        WHERE (user_a = %s OR user_b = %s) AND status='connected'
    """, (user_id, user_id))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row[0] if row else None


def get_partner_id(user_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            CASE 
                WHEN user_a = %s THEN user_b
                ELSE user_a
            END AS partner_id
        FROM partners
        WHERE (user_a = %s OR user_b = %s) AND status='connected'
    """, (user_id, user_id, user_id))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result[0] if result else None
def link_partner(user_id, partner_username):
    conn = get_db()
    cur = conn.cursor()

    # Get partner user_id
    cur.execute("SELECT user_id FROM users WHERE username=%s", (partner_username,))
    partner = cur.fetchone()

    if not partner:
        cur.close()
        conn.close()
        return False, "No such user exists."

    partner_id = partner[0]

    # Check if already linked
    cur.execute("""
        SELECT pair_id FROM partners 
        WHERE (user_a=%s AND user_b=%s) OR (user_a=%s AND user_b=%s)
    """, (user_id, partner_id, partner_id, user_id))
    
    if cur.fetchone():
        cur.close()
        conn.close()
        return False, "Already linked."

    # Create new partner link
    cur.execute("""
        INSERT INTO partners (user_a, user_b, status, start_date)
        VALUES (%s, %s, 'connected', CURDATE())
    """, (user_id, partner_id))

    conn.commit()
    cur.close()
    conn.close()
    return True, "Partner linked successfully!"

