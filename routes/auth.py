from flask import request, abort, redirect, Blueprint
from flask_login import *

from .dto import RegisterRequestInput, LoginRequestInput, ResetPasswordRequestInput
from db_queries import create_user, find_by_email, check_password, change_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = RegisterRequestInput(**request.json)

    if data.username is None or data.email is None or data.password is None or len(data.password) < 3:
        abort(400)

    user = find_by_email(data.email)
    if user:
        abort(409)
    else:
        create_user(data.username, data.email, data.password)
        return "OK", 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = LoginRequestInput(**request.json)

    if data.email is None or data.password is None or len(data.password) < 3:
        abort(400)

    user = check_password(data.password, data.email)
    if user:
        login_user(user, remember=True)
        return redirect('/locations')
    else:
        abort(409)


@login_required
@auth_bp.route('/reset', methods=['POST'])
def reset():
    data = ResetPasswordRequestInput(**request.json)
    if data.email is None or len(data.password) < 3:
        abort(409)

    email = data.email
    password = data.password

    user = find_by_email(email)
    if user:
        change_password(password, email)
        return redirect('/locations')
    else:
        abort(409)