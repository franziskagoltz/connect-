""" datamodel for conntect++ """

from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, pprint


# connection to the PostgreSQL database
db = SQLAlchemy()


# Model definitions
class User(db.Model):
    """Users of connect++"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fb_id = db.Column(db.String(100))
    fb_token = db.Column(db.String(200))
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    picture_url = db.Column(db.String(200))

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
    email = db.Column(db.String(100))
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

    @classmethod
    def serialize_connections_object(cls, connections):

        schema = ConnectionSchema(many=True)
        # result = []
        # for connection in connections:
        result = schema.dump(connections)

        return result

    @classmethod
    def get_connection(cls, connection_id, user_id):
        """returns a connection instance from db"""

        return Connection.query.filter_by(connection_id=connection_id, user_id=user_id).one()

    @classmethod
    def search_connections(cls, search_term, user_id):
        """queries the db to return a list of connections that match a search term"""

        return Connection.query.filter(Connection.user_id == user_id, (
            Connection.first_name.ilike("%"+search_term+"%")) |
            (Connection.last_name.ilike("%"+search_term+"%"))).all()


class ConnectionSchema(Schema):
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()
    met_where = fields.Str()
    introduced_by = fields.Str()
    connection_added_at = fields.DateTime()
    city = fields.Str()
    state = fields.Str()
    notes = fields.Str()
    interests = fields.Str()

    def __repr__(self):
        return "ConnectionSchema instantiated"


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
