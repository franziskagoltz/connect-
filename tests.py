import unittest
from server import app


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


if __name__ == "__main__":

    unittest.main()
