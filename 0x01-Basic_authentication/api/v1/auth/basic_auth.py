#!/usr/bin/env python3
'''Class for basic authentication'''
from api.v1.auth.auth import Auth


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
