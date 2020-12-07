from flask import Flask, request, redirect, flash, session, render_template
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm
from models import db, connect_db, Pet, DEFAULT_IMG

app = Flask(__name__, static_url_path='/static')

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def list_pets():
    """render home page which shows list of all pets"""
    # get all pets
    pets = Pet.query.order_by(Pet.id).all()
    return render_template('index.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Add a new pet to the site"""
    form = AddPetForm()

    if form.validate_on_submit():
        # use dict unpacking with **kwargs to initialize pet from form
        pet_data = {k: v for k, v in form.data.items() if k != 'csrf_token'}
        new_pet = Pet(**pet_data)

        if new_pet.photo_url == '':
            new_pet.photo_url = None

        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('add_pet.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def show_pet_details(pet_id):
    """show pet details and render form for editing"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        if pet.photo_url == '':
            pet.photo_url = DEFAULT_IMG
        db.session.commit()
        return redirect('/')
    else:
        return render_template('edit_pet.html', form=form, pet=pet)
