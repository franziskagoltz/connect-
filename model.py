""" datamodel for conntect++ """

from flask_sqlalchemy import SQLAlchemy


# connection to the PostgreSQL database
db = SQLAlchemy()


# Model definitions
class Users(db.Model):
    """Users of connect++"""

    __tabelname__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "User id={} email={} password={} zipcode={}".format(
            self.user_id, self.first_name, self.last_name)


# Helper functions to connect to database

def connect_to_db(app, database_uri):
    """Connect the database to our Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # running when file gets called directly

    from server import app
    connect_to_db(app, "postgresql:///connect")
    print "Connected to DB."
