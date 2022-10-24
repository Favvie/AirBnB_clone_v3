# #!/usr/bin/python3
# """
# a new view for City objects that handles all default RESTFul API actions
# """
# from models.city import City
# from models.state import State
# from models import storage
# from api.v1.views import app_views
# from flask import abort, jsonify, make_response, request
# from flasgger.utils import swag_from


# @app_views.route('/states/<state_id>/cities', methods=['GET'], 
#                  strict_slashes=False)
# @swag_from('documentation/city/cities_by_state.yml', methods=['GET'])
# def get_cities(state_id):
#     """ gets cities from state, if no state, abort """
#     list_cities = []
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     for city in state.cities:
#         list_cities.append(city.to_dict())

#     return jsonify(list_cities)

# @app.views.route('/cities/<city_id>', method=['GET'], strict_slashes=False)
# @swag_from('documentation/city/get_city.yml', methods=['GET'])
# def get_cities(city_id):
#     """ gets cities from City, If not linked to city, abort """
#     city = storage.get(City, city_id)
#     if not city:
#         abort(404)

#     return jsonify(city.to_dict())

# @app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
# @swag_from('documentation/city/delete_city.yml', methods=['DELETE'])
# def delete_cities(city_id):
#     """ deletes city from city dict """
#     city = storage.get(City, city_id)
#     if not city:
#         abort(404)

#     storage.delete(city)
#     storage.save

#     return make_response(jsonify({}), 200)

# @app_views.route('/states/<state_id>/cities', methods=['POST'],
#                  strict_slashes=False)
# @swag_from('documentation/city/post_city.yml', methods=['POST'])
# def post_city(state_id):
#     """ post city to states and under cities """
#     state = storage.get(State, state_id)
#     if not state:
#         abort(404)
#     if not request.get_json():
#         abort(400, description="Not a JSON")
#     if 'name' not in request.get_json():
#         abort(400, description="Missing name")

#     city = request.get_json()
#     point = City(**city)
#     point.state_id = state.id
#     point.save()
#     return make_response(jsonify(point.to_dict()), 201)

# @app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
# @swag_from('documentation/city/put_city.yml', methods=['PUT'])
# def put_city(state_id):
#     """ put city to states and under cities """
#     city = storage.get(City, city_id)
#     if not city:
#         abort(404)
#     if not request.get_json():
#         abort(400, description="Not a JSON")

#     discard = ['id', 'state_id', 'created_at', 'updated_at']

#     data = request.get_json()
#     for key, value in data.items():
#         if key not in discard:
#             setattr(city, key, value)
#     storage.save()
#     return make_response(jsonify(city.to_dict()), 200)