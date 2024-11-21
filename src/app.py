from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

@app.route('/success/<url>')
def success(url):
    return 'Shortened URL:  "http://127.0.0.1:5000/url/ %s' % url

@app.route('/url/<url>')
def access_url(url):
    return redirect('http://www.google.com')

@app.route('/create_url', methods=['GET', 'POST'])
def create_url():
    if request.method == 'POST':
        long_url = request.form['url']
        return redirect(url_for('success', url="ADFR"))
    else:
        long_url = request.args.get('url')
        return redirect(url_for('success', url="ADFR"))

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def index():
    return render_template("index.html")