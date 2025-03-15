import json
from flask import request, redirect, jsonify, abort, make_response, Blueprint
from flask_login import login_required

from db_queries import (find_user_by_id, create_location, get_locations_db,
                        find_location_by_id, delete_location_by_id, find_liked_reactions_in_location,
                        find_disliked_reactions_in_location, find_location_by_category, put_location_db,
                        search_location)
from .dto import LocationRequestInput, LocationSelectedRatingInput


location_bp = Blueprint('location', __name__)


@location_bp.route('/location/<int:id>', methods=['POST'])
@login_required
def post_location(id):
    data = LocationRequestInput(**request.json)
    user = find_user_by_id(id)
    if user is None:
        abort(404)
    else:
        create_location(data.name, data.description, data.category, user.id)
        return redirect('/locations')


@location_bp.route('/locations')
def get_locations():
    locations = get_locations_db()
    if locations:
        locations_json = [
            {
                'name': location.name,
            } for location in locations
        ]
        return jsonify(locations_json), 200
    else:
        return {'message': 'No locations found'}, 404


@location_bp.route('/location/<int:id>')
def get_location(id):
    location = find_location_by_id(id)
    if location:
        location_json = {
            'id': location.name
        }
        return jsonify(location_json), 200
    else:
        return {'message': 'No location found'}, 404


@location_bp.route('/location/<int:id>', methods=['PUT'])
@login_required
def put_location(id):
    location = find_location_by_id(id)
    if location:
        data = LocationRequestInput(**request.json)
        location.name = data.name if data.name else location.name
        location.description = data.description if data.description else location.description
        location.category = data.category if data.category else location.category
        put_location_db(location)
        return redirect('/locations')
    else:
        return {'message': 'No location found'}, 404


@location_bp.route('/location/<int:id>', methods=['DELETE'])
@login_required
def delete_location(id):
    location = find_location_by_id(id)
    if location:
        delete_location_by_id(id)
        return redirect('/locations')
    else:
        return {'message': 'No location found'}, 404


@location_bp.route('/top_locations')
def get_top_locations():
    locations = get_locations_db()
    if locations is None:
        return {'message': 'No locations found'}, 404

    rating_list = []

    for location in locations:
        like_count = find_liked_reactions_in_location(location.id)
        dislike_count = find_disliked_reactions_in_location(location.id)

        rating = 1.0 if dislike_count == 0 else like_count / (like_count + dislike_count)

        rating_list.append((location.name, rating))

    sorted_locations = sorted(rating_list, key=lambda x: x[1], reverse=True)

    return jsonify(dict(sorted_locations)), 200


@location_bp.route('/selected-rating', methods=['POST'])
def get_locations_by_selected_rating():
    data = LocationSelectedRatingInput(**request.json)
    if not data or 'rating' not in data:
        return {'message': 'Invalid input'}, 400

    selected_rating = data['rating']
    locations = get_locations_db()
    if locations is None:
        return {'message': 'No locations found'}, 404

    filtered_locations = {}

    for location in locations:
        like_count = find_liked_reactions_in_location(location.id)
        dislike_count = find_disliked_reactions_in_location(location.id)

        rating = 1.0 if dislike_count == 0 else like_count / (like_count + dislike_count)

        if rating > selected_rating:
            filtered_locations[location.name] = rating

    return jsonify(filtered_locations), 200


@location_bp.route('/location/<string:category>', methods=['GET'])
def get_location_category(category):
    locations = find_location_by_category(category)
    if locations is None:
        return {'message': 'No locations found'}, 404
    else:
        location_json = [
            {
                'name': location.name,
            } for location in locations
        ]
        return jsonify(location_json)


@location_bp.route('/search')
def search():
    db_query = request.args.get('q', '').strip()

    if db_query:
        results = search_location(db_query)
        results_json = [
            {
                'name': location.name,
                'description': location.description
            } for location in results
        ]
        return jsonify(query=db_query, reults=results_json), 200
    else:
        return {'message': 'No location found'}, 404


@location_bp.route('/locations/load_json')
def load_locations_json():
    locations = get_locations_db()
    if locations is None:
        return {'message': 'No locations found'}, 404

    locations_list = [{'id': loc.id, 'name': loc.name, 'description': loc.description, 'category': loc.category} for loc in locations]
    json_data = json.dumps(locations_list, ensure_ascii=False, indent=4)
    response = make_response(json_data)
    response.headers['Content-Disposition'] = 'attachment; filename=locations.json'
    response.headers['Content-Type'] = 'application/json'
    return response