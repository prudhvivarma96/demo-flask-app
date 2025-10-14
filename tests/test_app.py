# tests/test_app.py
import unittest
from app import app

class TestApp(unittest.TestCase):

    def test_index(self):
        tester = app.test_client()
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello', response.data)

if __name__ == "__main__":
    unittest.main()

