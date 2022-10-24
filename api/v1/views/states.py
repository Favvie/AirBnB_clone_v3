#!/usr/bin/python3
"""view for state objects that handles all default restful api actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    storage.reload()
    arr = []
    for obj in storage.all(State).values():
        arr.append(obj.to_dict())
    return jsonify(arr)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def single_state(state_id):
    """return json for a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Create and add a new review for a place"""

    if not request.get_json():
        abort(404, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    state = request.get_json()
    instance = State(**state)
    instance.save()
    storage.new(instance)
    storage.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """ puts new info in an amenity """
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'created_at', 'updated_at']

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
