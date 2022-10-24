#!/usr/bin/python3
"""index module for app view"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenity": Amenity, "city": City, "place": Place,
           "review": Review, "state": State, "user": User}


@app_views.route('/status', strict_slashes=False)
def status():
    """method to return status of route"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """count the number of instances for each class"""
    classes_count = {}
    for key, value in classes.items():
        classes_count[key] = storage.count(value)
    return jsonify(classes_count)
