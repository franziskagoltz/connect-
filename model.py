""" datamodel for conntect++ """

from flask_sqlalchemy import SQLAlchemy


# connection to the PostgreSQL database
db = SQLAlchemy()


# Model definitions
class User(db.Model):
    """Users of connect++"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    connections = db.relationship("Connection", backref="users")

    def __repr__(self):
        return "User id={} first_name={} last_name={}".format(
            self.user_id, self.first_name, self.last_name)


class Connection(db.Model):
    """Connections of each User"""

    __tablename__ = "connections"

    connection_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = email = db.Column(db.String(100))
    met_where = db.Column(db.String(100))
    introduced_by = db.Column(db.String(100))
    connection_added_at = db.Column(db.DateTime)
    city = db.Column(db.String(25))
    state = db.Column(db.String(2))
    notes = db.Column(db.String)
    interests = db.Column(db.String(500))

    def __repr__(self):
        return "Connection id={} first_name={} last_name={}".format(
            self.connection_id, self.first_name, self.last_name)


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
    db.create_all()
