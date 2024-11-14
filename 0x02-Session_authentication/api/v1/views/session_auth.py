#!/usr/bin/env python3
'''view to handle all routes for Session Authentication'''
from api.v1.views import app_views
from models.user import User
import os
from flask import request, jsonify, make_response, Blueprint, abort


session_auth = Blueprint('session_auth', __name__)


@app_views.route('/auth_session/login', strict_slashes=False, methods=['POST'])
def session_login():
    '''login after session authentication'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not email or email is None:
        return jsonify({"error": "email missing"}), 400
    if not password or password is None:
        return jsonify({"error": "password missing"}), 400

    # Get user using email
    users = User.search({'email': email})
    if not users or users is None:
        return jsonify({"error": "no user found for this email"}), 404
    user = users[0]  # if users is a list

    # check user email
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # get session id
    from api.v1.app import auth
    session_id = auth.create_session(user.id)

    # create response
    response = make_response(user.to_json())
    session_name = os.getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response

@app_views.route(
        '/auth_session/logout', strict_slashes=False, methods=['DELETE'])
def logout():
    from api.v1.app import auth
    bool_value = auth.destroy_session(request)
    if bool_value is False:
        return False, abort(404)
    return jsonify({})
