#!/usr/bin/python3
"""
new view for Amenity objects that handles all default RESTFul API actions
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenities/get_amenities.yml', methods=['GET'])
def get_amenities():
    """ get list of amenities """
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenities/get_amenities.yml', methods=['GET'])
def get_amenities(amenity_id):
    """ gets amenities through amenities_id, if not in amenity, abort """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenities.yml', methods=['DELETE'])
def delete_amenities(amenity_id):
    """ deletes amenities """
    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)
    storage.delete(amenities)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenities.yml', methods=['POST'])
def post_amenities():
    """ Post new amenities """
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    amenities = request.get_json()
    instance = Amenity(**amenities)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put_amenities.yml', methods=['PUT'])
def put_amenities(amenity_id):
    """ puts new info in an amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'created_at', 'updated_at']

    amenities = storage.get(Amenity, amenity_id)
    if not amenities:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(amenities, key, value)
    storage.save()
    return make_response(jsonify(amenities.to_dict()), 200)
