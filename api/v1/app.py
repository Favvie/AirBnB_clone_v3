#!/usr/bin/python3
"""root app documentation"""

from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_session(exc):
    """close storage after each session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """custom error handler"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=(os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=(os.getenv("HBNB_API_PORT", "5000"), threaded=True)
