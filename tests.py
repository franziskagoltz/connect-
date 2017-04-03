import unittest
from datetime import datetime
from flask import Flask, jsonify, session
from flask.ext.bcrypt import Bcrypt
from model import connect_to_db, db, User, Connection
import helper
from server import app


# app = Flask(__name__)
bcrypt = Bcrypt(app)


class FlaskTestLoggedOut(unittest.TestCase):
    """Testing Flask Routes when user is not logged in"""

    def setUp(self):
        """Happens before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_landing(self):
        """Test landing page of connect++ without being login"""

        result = self.client.get("/")
        self.assertIn("Welcome to Connect++", result.data)

    def test_signup(self):
        """Test signup page of connect++ without being login"""

        result = self.client.get("/sign-up")
        self.assertIn("Sign up to Connect++", result.data)

    def test_login(self):
        """Test login page of connect++ without being login"""

        result = self.client.get("/login")
        self.assertIn("Login", result.data)

    def test_add_connection(self):
        """Test add connection page of connect++ without login"""

        result = self.client.get("/add-connection", follow_redirects=True)
        self.assertIn("Please log in to add a new connection", result.data)
        self.assertIn("Welcome to Connect++", result.data)

    def test_search_connections(self):
        """Test search connection feature of connect++ without login"""

        result = self.client.get("/search", follow_redirects=True)
        self.assertIn("Please log in to search for connections", result.data)
        self.assertIn("Login", result.data)

    def test_view_connections(self):
        """Test view connections feature of connect++ without login"""

        result = self.client.get("/view-connections", follow_redirects=True)
        self.assertIn("Please log in to view connections", result.data)
        self.assertIn("Login", result.data)

    def test_view_connection_details(self):
        """Test view connection details feature of connect++ without login"""

        result = self.client.get("/connection/1", follow_redirects=True)
        self.assertIn("Please log in to view connection details", result.data)
        self.assertIn("Login", result.data)


class FlaskTestLoggedIn(unittest.TestCase):
    """Testing Flask Routes when user is logged in"""

    def setUp(self):
        """Happens before every test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1
                sess["user_name"] = "UserName"

    def test_landing(self):
        """Test landing page of connect++ when logged in"""

        result = self.client.get("/")
        self.assertIn("You're signed in as", result.data)

    def test_add_connection(self):
        """Test add connection page of connect++ when logged in"""

        result = self.client.get("/add-connection")
        self.assertIn("Add a New Connection", result.data)


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config["TESTING"] = True

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1
                sess["user_name"] = "UserName"

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_view_connections(self):
        """Test view connections feature of connect++ when logged in"""

        result = self.client.get("/view-connections", follow_redirects=True)
        self.assertIn("Your Connections", result.data)
        # self.assertIn("Login", result.data)

    def test_view_connection_details(self):
        """Test view connections feature of connect++ when logged in"""

        result = self.client.get("/connection/1")
        self.assertIn("Details", result.data)
        self.assertIn("Lotta", result.data)

    def test_search_connections(self):
        """Test search connection feature of connect++ when logged in"""

        result = self.client.get("/search?search=lotta", follow_redirects=True)
        self.assertIn("Your Connections", result.data)
        self.assertIn("You have 1 connections matching", result.data)

    def test_added_route(self):
        """test flask route that adds connection"""

        result = self.client.post("/added", data={"first_name": "Sammie",
                                                  "last_name": "Salt",
                                                  "email": "sammie@sammie.com",
                                                  "met_where": "techcrunch",
                                                  "introduced_by": "Liza",
                                                  "city": "SF",
                                                  "state": "CA",
                                                  "notes": "",
                                                  "interests": ""}, follow_redirects=True)
        self.assertIn("You added", result.data)
        self.assertIn("Your Connections", result.data)


def example_data():
    """loads example data into the db"""

    # User Data
    user = User(first_name="Jane", last_name="Hacks", email="jane@gmail.com",
                password=bcrypt.generate_password_hash("jane"))
    db.session.add(user)
    db.session.commit()

    # Connection Data
    connection1 = Connection(user_id=1, first_name="Lotta", last_name="Lemon",
                             email="lotta@lotta.com", met_where="techcrunch",
                             introduced_by="Tom", city="SF", state="CA", notes="",
                             interests="", connection_added_at=datetime.now())

    db.session.add(connection1)
    db.session.commit()


if __name__ == "__main__":

    unittest.main()
