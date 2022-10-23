#!/usr/bin/python3
"""root app documentation"""

from models import storage
from api.v1.views import app_views
from flask import Flask
import os

app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def close_session(exc):
    """close storage after each session"""
    storage.close()


if __name__ == "__main__":
    app.run(host=(os.getenv("HBNB_API_HOST") or "0.0.0.0"), port=(os.getenv("HBNB_API_PORT") or 5000), threaded=True)