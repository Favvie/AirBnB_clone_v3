#!/usr/bin/python3
"""a view for the user object and related api actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, make_response, abort
from flasgger.utils import swag_from
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
@swag_from('documentation/amenities/get_amenities.yml', methods=['GET'])
def amenities():
    """return all amenities instances"""
    list_amenities = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
@swag_from('documentation/amenities/get_amenity.yml', methods=['GET'])
def amenity(amenity_id):
    """return a amenity instance"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/amenities/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """delete a amenity from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/amenities/post_amenity.yml', methods=['POST'])
def post_amenity():
    """post amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    amenity = request.get_json()
    instance = Amenity(**amenity)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
@swag_from('documentation/amenities/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """ update amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)


if __name__ == "__main__":
    pass
