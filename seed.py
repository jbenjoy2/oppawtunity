from models import Pet, db
from app import app

# create all tables
db.drop_all()
db.create_all()

roscoe = Pet(name='Roscoe', species='dog', age=15, available=True)

db.session.add(roscoe)
db.session.commit()
