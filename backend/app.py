from flask import Flask, render_template, request, redirect, url_for, flash
# from sqlalchemy.orm import Session, sessionmaker

app = Flask(__name__)
app.secret_key = 'magickey'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/news")
def news():
    return render_template('news.html')

@app.route("/wiki")
def wiki():
    return render_template('wiki.html')

@app.route("/ar")
def ar():
    return render_template('ar.html')

@app.route("/user")
def user():
    return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)