import sqlite3
from datetime import datetime
from dateutil.relativedelta import relativedelta

def check_expiry(hash):
    """
    Check if the URL associated with the given hash has expired.

    Args:
        hash (str): The hash of the URL to check.

    Returns:
        bool: True if the URL has expired, False otherwise.
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT expiry < datetime('now') FROM urls WHERE hash = ?", (hash,))
    output = result.fetchone()
    if output and output[0] == 1:
        return True
    else:
        return False

def fetch_url(hash):
    """
    Fetches the long URL corresponding to the given hash from the database.

    Args:
        hash (str): The hash value used to look up the long URL in the database.

    Returns:
        str: The long URL if found, otherwise an empty string.
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT long_url FROM urls WHERE hash = ?", (hash,))
    output = result.fetchone()
    if not output:
        return ""
    return output[0]

def check_availability(hash):
    """
    Check if a given hash is available in the 'urls' table of the 'url.db' database.

    Args:
        hash (str): The hash value to check for availability.

    Returns:
        bool: True if the hash is not present in the 'urls' table, False otherwise.
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    result = c.execute("SELECT EXISTS (SELECT 1 from urls WHERE hash = ?)", (hash,))
    return True if result.fetchone()[0] == 0 else False

def insert_url(hash, long_url, short_url, expiry):
    """
    Inserts a URL record into the database.

    Args:
        hash (str): The unique hash for the URL.
        long_url (str): The original long URL.
        short_url (str): The shortened URL.
        expiry (str): The expiry date in the format 'YYYY-MM-DD'. If None, the expiry date will be set to one year from the current date.

    Returns:
        None
    """
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

def delete_url(hash):
    """
    Deletes a URL entry from the 'urls' table in the 'url.db' SQLite database based on the provided hash.

    Args:
        hash (str): The hash value of the URL entry to be deleted.

    Returns:
        None
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE hash = ?", (hash,))
    conn.commit()

def delete_expired_urls():
    """
    Deletes expired URLs from the 'urls' table in the 'url.db' SQLite database.

    This function connects to the 'url.db' SQLite database, executes a SQL 
    DELETE statement to remove rows from the 'urls' table where the 'expiry' 
    column is less than the current datetime, and commits the changes.

    Raises:
        sqlite3.DatabaseError: If there is an issue with the database connection 
        or execution of the SQL statement.
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute("DELETE FROM urls WHERE expiry < datetime('now')")
    conn.commit()