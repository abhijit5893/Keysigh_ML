from flask import Flask, redirect, url_for, request, render_template
import secrets
import string

app = Flask(__name__)

format = 'utf-8'
length = 8
chars = string.ascii_letters + string.digits + '-'

@app.route('/success/<url>')
def success(url):
    return 'Shortened URL: http://127.0.0.1:5000/url/%s' % url

@app.route('/url/<url>')
def access_url(url):
    return redirect('http://www.google.com')

def hash(input):
    short = ''.join(secrets.choice(chars) for i in range(length))
    return short

@app.route('/create_url', methods=['GET', 'POST'])
def create_url():
    if request.method == 'POST':
        long_url = request.form['url']
        return redirect(url_for('success', url=hash(long_url)))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")