import sqlite3

def check_expiry(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT expiry < datetime('now') FROM urls WHERE hash = ?", (hash,))
    return True if result.fetchone()[0] == 1 else False

def fetch_url(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT long_url FROM urls WHERE hash = ?", (hash,))
    return result.fetchone()

def check_availability(hash):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT EXISTS (SELECT 1 from urls WHERE hash = ?)", (hash,))
    return True if result.fetchone()[0] == 0 else False

def insert_url(hash, long_url, short_url):
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute("INSERT INTO urls VALUES (?, ?, ?, datetime('now'), datetime('now', '-1 minute'))", (hash, long_url, short_url))
    conn.commit()