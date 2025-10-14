import unittest
from app import app
import werkzeug
# Patch missing __version__ attribute for Flask test client compatibility
if not hasattr(werkzeug, "__version__"):
    werkzeug.__version__ = "2.2.3"

