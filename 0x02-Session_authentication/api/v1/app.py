#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth = os.getenv('AUTH_TYPE')
if auth == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth == 'session_auth':
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()

# Define list of paths that do not require authentication
excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    '''Unauthorized entry of user'''
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    '''Forbidden resource from a user'''
    return jsonify({"error": "Forbidden"}), 403


@app.route('/api/v1/status', methods=['GET'])
def get_status():
    '''endpoint for api status'''
    return jsonify({"status": "OK"}), 200


@app.before_request
def before_request():
    '''Function to check if user is authorized'''
    if auth is None:
        return
    # check if the request needs authorization
    if auth.require_auth(request.path, excluded_paths):
        # check if request authorization
        if auth.authorization_header(request) is None:
            abort(401)
        # if there's is not current user
        if auth.current_user(request) is None:
            abort(403)
        else:
            request.current_user = auth.current_user(request)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
