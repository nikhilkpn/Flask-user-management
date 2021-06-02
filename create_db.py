import os
from config import db
from models import User

# Data to initialize database with
USER = [
    {"first_name": "Nikhil", "last_name": "K.P"},
    {"first_name": "Akhil", "last_name": "George"},
    {"first_name": "Sunny", "last_name": "K"},
]

# Delete database file if it exists currently
if os.path.exists("user.db"):
    os.remove("user.db")

# Create the database
db.create_all()

# iterate over the USER structure and populate the database
for user in USER:
    p = User(last_name=user.get("last_name"), first_name=user.get("first_name"))
    db.session.add(p)

db.session.commit()