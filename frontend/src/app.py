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

@app.route("/user")
def user():
    return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)