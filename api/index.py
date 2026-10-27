import os
import sys

# Add root directory to sys.path so app.py and templates/static can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Vercel requires the WSGI app instance named 'app'
app = app
