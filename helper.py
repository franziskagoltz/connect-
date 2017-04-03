"""helper functions to be used in server.py"""

from model import connect_to_db, db, User, Connection
from flask import Flask, jsonify, session
from datetime import datetime
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# db.create_all()


def add_connection(info, user_id):
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

    connection = Connection(user_id=user_id, first_name=first_name, last_name=last_name,
                            email=email, met_where=met_where, introduced_by=introduced_by,
                            city=city, state=state, notes=notes, interests=interests,
                            connection_added_at=connection_added_at)

    db.session.add(connection)

    db.session.commit()


def get_connections(user_id):
    """gets all of a users connections from the db"""

    connections = Connection.query.filter_by(user_id=user_id).all()

    return connections


def get_cities_of_connections(connections):
    """returns a set of all the cities a user has a connection in"""

    return {connection.city for connection in connections}


def get_city_connection_pairs(city, user_id):
    """maps together cities and connections: who do you know in each city?"""

    connections_by_city = Connection.query.filter_by(user_id=user_id, city=city).all()

    return connections_by_city


def add_user(info):
    """adds a new user to the database"""

    for data in info:
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        email = info.get("email")
        password = info.get("password", "passwordfromfb")
        fb_id = info.get("fb_id")
        picture_url = info.get("picture_url")
        fb_token = info.get("fb_token")

    user = User(first_name=first_name, last_name=last_name, email=email,
                password=bcrypt.generate_password_hash(password), fb_token=fb_token,
                fb_id=fb_id, picture_url=picture_url)

    db.session.add(user)

    db.session.commit()

    return user


def get_current_user(email, password):
    """getting the current user from the database"""

    stored_pwhash = User.query.filter(User.email == email).one().password

    if bcrypt.check_password_hash(stored_pwhash, password):

        return User.query.filter(User.email == email).one()
