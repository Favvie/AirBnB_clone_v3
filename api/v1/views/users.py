#!/usr/bin/python3
"""a view for the user object and related api actions"""

from api.v1.views import app_views
from models import storage
from flask import jsonify, request, make_response, abort
from flasgger.utils import swag_from
from models.user import User


@app_views.route('/users', strict_slashes=False)
@swag_from('documentation/users/get_users.yml', methods=['GET'])
def users():
    """return all user instances"""
    list_users = []
    users = storage.all(User).values()
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', strict_slashes=False)
@swag_from('documentation/users/get_user.yml', methods=['GET'])
def user(user_id):
    """return a user instance"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/users/delete_user.yml', methods=['DELETE'])
def delete_user(user_id):
    """delete a user from storage"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/users/post_user.yml', methods=['POST'])
def post_user():
    """post user"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing email")

    user = request.get_json()
    instance = User(**user)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/users/put_user.yml', methods=['PUT'])
def put_user(user_id):
    """ update user object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'email', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)


if __name__ == "__main__":
    pass
