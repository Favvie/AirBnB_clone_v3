#!/usr/bin/python3
"""index module for app view"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def status():
    """method to return status of route"""
    return jsonify({"status": "OK"})
