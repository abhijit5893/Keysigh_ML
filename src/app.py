from flask import Flask, redirect, url_for, request, render_template
import secrets
import string
from db_util import *

app = Flask(__name__)

with app.app_context():
    """
    Runs one time before the first request to the application.
    """
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls \
            (hash TEXT, long_url TEXT, short_url TEXT, created_on TEXT, expiry TEXT, PRIMARY KEY(hash))''')
    conn.commit()

format = 'utf-8'
length = 8
chars = string.ascii_letters + string.digits

@app.route('/success/<url>')
def success(url):
    """
    Generates an HTML string for a shortened URL.

    Args:
        url (str): The shortened URL path.

    Returns:
        str: An HTML string containing the shortened URL link.
    """
    return 'Shortened URL: <a href="http://127.0.0.1:5000/url/%s"> http://127.0.0.1:5000/url/%s </a>' %( url, url)

@app.route('/url/<url>')
def access_url(url):
    """
    Accesses a given URL, checks if it has expired, and redirects to the long URL if it hasn't expired.

    Args:
        url (str): The shortened URL to be accessed.

    Returns:
        str: A message indicating that the URL has expired, or a redirect to the long URL.
    """
    if check_expiry(url):
        delete_url(url)
        return 'URL has expired'
    long_url = fetch_url(url)
    return redirect(long_url)

def hash(input):
    """
    Generates a random hash string.

    Args:
        input: The input value to be hashed (not used in the current implementation).

    Returns:
        str: A randomly generated hash string.
    """
    short = ''.join(secrets.choice(chars) for i in range(length))
    return short


@app.route('/create_url', methods=['GET', 'POST'])
def create_url():
    """
    Handles the creation of a shortened URL.

    If the request method is POST, it retrieves the long URL and expiry date from the form data,
    generates a hash for the long URL, and checks if the hash is available. If available, it inserts
    the URL data into the database and redirects to the success page with the shortened URL hash.
    If the hash is not available, it redirects back to the URL creation page.

    Returns:
        Response: A redirect to the success page with the shortened URL hash if the URL is successfully
                  shortened, or a redirect back to the URL creation page if the hash is not available.
                  If the request method is not POST, it renders the index page.
    """
    if request.method == 'POST':
        long_url = request.form['url']
        expiry = request.form['expiry']
        short_url_hash = hash(long_url)
        if check_availability(short_url_hash):
            insert_url(short_url_hash, long_url, short_url_hash, expiry)
            return redirect(url_for('success', url=short_url_hash))
        else:
            return redirect(url_for('create_url'))
    return render_template('index.html')

if __name__ == '__main__':    
    app.run(debug=True)

@app.route("/")
def index():
    """
    Renders the index.html template.

    Returns:
        str: The rendered HTML content of the index page.
    """
    return render_template("index.html")

