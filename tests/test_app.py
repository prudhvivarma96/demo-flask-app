import unittest
from app import app
import werkzeug

# Patch missing attribute for Flask test client compatibility
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "2.2.3"

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

