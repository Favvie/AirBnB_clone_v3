#!/usr/bin/python3
"""view for state objects that handles all state api actions"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, request, make_response, abort


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    storage.reload()
    arr = []
    for obj in storage.all(Amenity).values():
        arr.append(obj.to_dict())
    return jsonify(arr)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def single_amenity(amenity_id):
    """return json for a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create and add a new amenity"""

    if not request.get_json():
        abort(404, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    amenity = request.get_json()
    instance = Amenity(**amenity)
    instance.save()
    storage.new(instance)
    storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """ puts new info in an amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'created_at', 'updated_at']

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)


if __name__ == "__main__":
    pass
