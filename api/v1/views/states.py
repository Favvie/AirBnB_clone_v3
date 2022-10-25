#!/usr/bin/python3
"""a view for the state object and related api actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, make_response, abort
from flasgger.utils import swag_from
from models.state import State


@app_views.route('/states', strict_slashes=False)
@swag_from('documentation/states/get_states.yml', methods=['GET'])
def states():
    """return all user instances"""
    list_states = []
    states = storage.all(State).values()
    for state in states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route('/states/<state_id>', strict_slashes=False)
@swag_from('documentation/states/get_state.yml', methods=['GET'])
def state(state_id):
    """return a state instance"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/states/delete_state.yml', methods=['DELETE'])
def delete_state(state_id):
    """delete a state from storage"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/states/post_state.yml', methods=['POST'])
def post_state():
    """post state"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    state = request.get_json()
    instance = State(**state)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/states/put_state.yml', methods=['PUT'])
def put_state(state_id):
    """ update state object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


if __name__ == "__main__":
    pass
