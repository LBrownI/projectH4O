import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from time import sleep
import checkPlant
# from sqlalchemy.orm import Session, sessionmaker

app = Flask(
    __name__, 
    template_folder=os.path.join(os.getcwd(), 'frontend', 'src', 'templates'),
    static_folder=os.path.join(os.getcwd(), 'frontend', 'src', 'static')
)

app.secret_key = 'magickey'
# Configure the uploads folder
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'backend', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Create the uploads folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/scanplant", methods=["GET", "POST"])
def scanplant():
    if request.method == "POST":
        # Check if a file was uploaded
        if 'plantImage' not in request.files:
            flash("No file part")
            return redirect(request.url)
        
        file = request.files['plantImage']

        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        # Save the file to the 'uploads' folder
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            flash(f"Image uploaded successfully: {filename}")
            return redirect(url_for('plant_info'))
        
        # data = checkPlant.test_checkPlant()
        # session['plant_data'] = data
        return redirect(url_for('plant_info'))

    return render_template('scanPlant.html')

@app.route('/plant_info')
def plant_info():
    # data = session.get('plant_data', {})
    data = checkPlant.test_checkPlant()
    # sleep(5)
    return render_template('plantInfo.html', data=data)

@app.route('/home')
def home():
    print("GOINF TO HOME")
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

# @app.route("/ar/scanplant")
# def scanplant():
#     return render_template('scanPlant.html')

@app.route("/user")
def user():
    return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)