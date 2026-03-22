from config import get_db
import datetime

def get_start_date(pair_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT start_date FROM partners WHERE pair_id=%s", (pair_id,))
    result = cur.fetchone()
    cur.close(); conn.close()
    return result[0] if result and result[0] else None

def days_together(start_date):
    today = datetime.date.today()
    return (today - start_date).days

def next_monthiversary(start_date):
    today = datetime.date.today()
    months = (today.year - start_date.year) * 12 + today.month - start_date.month
    next_date = (start_date.replace(day=1) + datetime.timedelta(days=32 * (months + 1))).replace(day=start_date.day)
    return (next_date - today).days

def next_anniversary(start_date):
    today = datetime.date.today()
    this_year_ann = start_date.replace(year=today.year)
    if this_year_ann < today:
        this_year_ann = this_year_ann.replace(year=today.year + 1)
    return (this_year_ann - today).days
from config import get_db

def get_start_date(pair_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT start_date FROM partners WHERE pair_id=%s", (pair_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row[0] if row else None

def set_start_date(pair_id, date):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("UPDATE partners SET start_date=%s WHERE pair_id=%s", (date, pair_id))
    conn.commit()
    cur.close()
    conn.close()
