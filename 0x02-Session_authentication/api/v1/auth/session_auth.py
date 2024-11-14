#!/usr/bin/env python3
'''Class for session authenntication'''
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''Class to hold methods for session authentication'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a session for the given user_is'''
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        # generate session id
        session_id = str(uuid.uuid4())

        # setting session id as key for user_id
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''Returns a user_id based on the session id given'''
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)

        return user_id

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value'''
        if request is None:
            return None
        # get session name for cookie in request
        session_name = self.session_cookie(request)
        if session_name is None:
            return None
        # get user id using session_name
        user_id = self.user_id_for_session_id(session_name)
        if user_id is None:
            return None
        # get user using user_id
        user = User.get(user_id)

        return user
