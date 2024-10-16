from flask import Flask, render_template, request, redirect, url_for, flash
# from sqlalchemy.orm import Session, sessionmaker

app = Flask(__name__)
app.secret_key = 'magickey'

@app.route('/')
def test():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)