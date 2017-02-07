"""helper functions to be used in server.py"""

from model import connect_to_db, db, User, Connection
from flask import Flask, jsonify, session
from datetime import datetime
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# db.create_all()


def add_connection(info):
    """adds a new connection to the database"""

    for data in info:
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        email = info.get("email")
        met_where = info.get("met_where")
        introduced_by = info.get("introduced_by")
        city = info.get("city")
        state = info.get("state")
        notes = info.get("notes")
        interests = info.get("interests")
    connection_added_at = datetime.now()

    connection = Connection(first_name=first_name, last_name=last_name, email=email,
                            met_where=met_where, introduced_by=introduced_by,
                            city=city, state=state, notes=notes, interests=interests,
                            connection_added_at=connection_added_at)

    db.session.add(connection)

    db.session.commit()


def get_current_user(email, password):
    """getting the current user from the database"""

    stored_pwhash = User.query.filter(User.email == email).one().password

    if bcrypt.check_password_hash(stored_pwhash, password):

        return User.query.filter(User.email == email).one()

