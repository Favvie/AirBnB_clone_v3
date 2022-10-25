#!/usr/bin/python3
"""a view for place object and api actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False)
@swag_from('documentation/place/places_by_cities.yml', methods=['GET'])
def get_places(city_id):
    """ gets places from city, if no city, abort """
    list_places = []
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            list_places.append(place.to_dict())
    return jsonify(list_places)


@app_views.route('/places/<place_id>', strict_slashes=False)
@swag_from('documentation/place/get_place.yml', methods=['GET'])
def place(place_id):
    """return a place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place/delete_place.yml', methods=['DELETE'])
def delete_place(place_id):
    """ deletes place from city """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place/post_place.yml', methods=['POST'])
def post_place(city_id):
    """post place to cities"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    else:
        body = request.get_json()
        user = storage.get(User, body["user_id"])
        if not user:
            abort(404)

    place = request.get_json()
    instance = Place(**place)
    instance.city_id = city_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/place/put_place.yml', methods=['PUT'])
def put_place(place_id):
    """ put place under cities """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


if __name__ == "__main__":
    pass
