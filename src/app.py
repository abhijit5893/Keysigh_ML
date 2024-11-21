from flask import Flask, redirect, url_for, request, render_template
import secrets
import string
from db_util import *

app = Flask(__name__)

with app.app_context():
    conn = sqlite3.connect('url.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls \
            (hash TEXT, long_url TEXT, short_url TEXT, created_on TEXT, expiry TEXT, PRIMARY KEY(hash))''')
    conn.commit()

format = 'utf-8'
length = 8
chars = string.ascii_letters + string.digits + '-'

@app.route('/success/<url>')
def success(url):
    return 'Shortened URL: http://127.0.0.1:5000/url/%s' % url

@app.route('/url/<url>')
def access_url(url):
    if check_expiry(url):
        delete_url(url)
        return 'URL has expired'
    long_url = fetch_url(url)
    return redirect(long_url)

def hash(input):
    short = ''.join(secrets.choice(chars) for i in range(length))
    return short


@app.route('/create_url', methods=['GET', 'POST'])
def create_url():
    if request.method == 'POST':
        long_url = request.form['url']
        expiry = request.form['expiry']
        short_url_hash = hash(long_url)
        if check_availability(short_url_hash):
            print("-----", expiry)
            insert_url(short_url_hash, long_url, short_url_hash, expiry)
            return redirect(url_for('success', url=short_url_hash))
        else:
            return redirect(url_for('create_url'))
    return render_template('index.html')

if __name__ == '__main__':    
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")

