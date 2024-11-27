from flask import Flask, render_template, request, redirect, url_for, flash
from queries import *

app = Flask(
    __name__, 
    template_folder=os.path.join(os.getcwd(), 'frontend', 'src', 'templates'),
    static_folder=os.path.join(os.getcwd(), 'frontend', 'src', 'static')
)
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

@app.route('/wiki')
def wiki():
    search_query = request.args.get('search')  # Get the search query from the URL
    
    if search_query:
        # Filter plants by common or scientific name, case insensitive
        plants = session.query(Plant).filter(
            (Plant.nombre_comun.ilike(f'%{search_query}%')) | 
            (Plant.nombre_cientifico.ilike(f'%{search_query}%'))
        ).all()
    else:
        # If no search query, fetch all plants
        plants = session.query(Plant).all()
    
    return render_template('wiki.html', plants=plants)

@app.route('/plant/<int:plant_id>')
def plant_detail(plant_id):
    # Get the plant and its related description and care information from the database
    plant = session.query(Plant).get(plant_id)
    if not plant:
        return render_template('error.html', message="Plant not found")
    
    # Fetch related data
    description = session.query(PlantDescription).filter_by(planta_id=plant.id).first()
    care = session.query(PlantCare).filter_by(planta_id=plant.id).first()

    # Render the template with all the data
    return render_template('plant_detail.html', plant=plant, description=description, care=care)


@app.route("/ar")
def ar():
    return render_template('ar.html')

@app.route("/user")
def user():
    return render_template('user.html')
if __name__ == '__main__':
    app.run(debug=True)