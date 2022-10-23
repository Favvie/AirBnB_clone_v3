#!/usr/bin/python3
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify

classes = {"amenity": Amenity, "city": City, "place": Place, "review": Review, "state": State, "user": User}

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def return_status():
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def return_count():
    classes_count = {}
    for key, value in classes.items():
        classes_count[key] = storage.count(value)
    return jsonify(classes_count)
