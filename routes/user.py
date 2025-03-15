from flask import request, jsonify, redirect, Blueprint
from flask_login import login_required

from .dto import UserPutRequestInput
from db_queries import update_user, delete_user_by_id, find_all_users, find_user_by_id


user_bp = Blueprint('user', __name__)

@user_bp.route('/users')
def get_users():
    users = find_all_users()
    if users:
        users_json = [
            {
                'username': user.username,
            } for user in users
        ]
        return jsonify(users_json), 200
    else:
        return {'message': 'No users found'}, 404


@user_bp.route('/user/<int:id>')
def get_user(id):
    user = find_user_by_id(id)
    if user:
        user_json = {
            'username': user.username,
            'email': user.email,
            'password': user.password
        }
        return jsonify(user_json), 200
    else:
        return {'message': 'User not found'}, 404


@user_bp.route('/user/<int:id>', methods=['PUT'])
@login_required
def put_user(id):
    user = find_user_by_id(id)
    if user:
        data = UserPutRequestInput(**request.json)
        user.username = data.username if data.username else user.username
        user.email = data.email if data.email else user.email
        user.password = data.password if data.password else user.password
        update_user(user)
        return redirect('/locations'), 200
    else:
        return {'message': 'User not found'}, 404


@user_bp.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
    user = find_user_by_id(id)
    if user:
        delete_user_by_id(id)
        return {'message': 'User deleted'}, 200
    else:
        return {'message': 'User not found'}, 404