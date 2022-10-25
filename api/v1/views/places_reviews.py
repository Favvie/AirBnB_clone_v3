#!/usr/bin/python3
"""a view for reviews object and api actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False)
@swag_from('documentation/reviews/reviews_by_places.yml', methods=['GET'])
def get_reviews(place_id):
    """ gets reviews about places, if no place, abort """
    list_reviews = []
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
@swag_from('documentation/review/get_review.yml', methods=['GET'])
def review(review_id):
    """return a review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/review/delete_review.yml', methods=['DELETE'])
def delete_review(review_id):
    """ deletes review from city """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/review/post_review.yml', methods=['POST'])
def post_review(place_id):
    """post review to places"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    else:
        body = request.get_json()
        user = storage.get(User, body["user_id"])
        if not user:
            abort(404)

    review = request.get_json()
    instance = Review(**review)
    instance.place_id = place_id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/review/put_review.yml', methods=['PUT'])
def put_review(review_id):
    """ put review under cities """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    discard = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in discard:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)


if __name__ == "__main__":
    pass
