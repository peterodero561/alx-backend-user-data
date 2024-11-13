#!/usr/bin/env python3
'''Class for authentication for users'''
from flask import request
from typing import List, TypeVar


class Auth:
    '''Used for authentication of users'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''check if path needs authorization'''
        if path is None:
            return True
        if not excluded_paths:
            return True
        # ensure path ends with slash
        if not path.endswith('/'):
            path += '/'
        # check if path is in excluded paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/'):
                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        '''check for authorization in header of path'''
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''check ceurrent user'''
        return None
