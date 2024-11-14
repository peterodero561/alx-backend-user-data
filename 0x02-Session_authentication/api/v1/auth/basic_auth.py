#!/usr/bin/env python3
'''Class for basic authentication'''
from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    '''class to be ussed in basic authentication'''
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        '''Convert authorization from base64'''
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        '''decodes the base 64 authorization header'''
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            val = base64.b64decode(base64_authorization_header).decode('utf-8')
            return val
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        '''Extract email and password from decoded authorization value'''
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        # everything checks out
        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
        except ValueError:
            return None, None
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        '''Return the User instance based on the email and password'''
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        # search the email
        users = User.search({'email': user_email})

        # check if a user was found
        if not users or len(users) == 0:
            return None

        user = users[0]  # if the user brings a list

        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        '''Overloads Auth an retrives the User instanse of a request'''
        # get Authorization from request
        authorization = self.authorization_header(request)
        if authorization is None:
            return None
        # get authorization header
        authorization_header = self.extract_base64_authorization_header(
                authorization)
        if authorization_header is None:
            return None
        # decode authorization error
        decode_auth_header = self.decode_base64_authorization_header(
                authorization_header)
        if decode_auth_header is None:
            return None
        # get credentials from decode authorization header
        email, psswd = self.extract_user_credentials(decode_auth_header)
        if email is None or psswd is None:
            return None
        # get user and load to current user
        user = self.user_object_from_credentials(email, psswd)
        if user is None:
            return None
        return user
