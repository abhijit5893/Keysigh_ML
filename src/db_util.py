import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

def check_expiry(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT expiry < datetime('now') FROM urls WHERE hash = ?", (hash,))
    output = result.fetchone()
    if output and output[0] == 1:
        return True
    else:
        return False

def fetch_url(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT long_url FROM urls WHERE hash = ?", (hash,))
    output = result.fetchone()
    if not output:
        return ""
    return output[0]

def check_availability(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT EXISTS (SELECT 1 from urls WHERE hash = ?)", (hash,))
    return True if result.fetchone()[0] == 0 else False

def insert_url(hash, long_url, short_url, expiry):
    now = datetime.now() 
    if expiry:	
        expiry_date = datetime.strptime(expiry, "%Y-%m-%d")
        expiry_date = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        expiry_date = now + relativedelta(years=1)
        expiry_date = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls VALUES (?, ?, ?, ?, ?)", (hash, long_url, short_url, now.strftime("%Y-%m-%d %H:%M:%S"), expiry_date))
    conn.commit()