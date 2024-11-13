#!/usr/bin/env python3
'''Class for basic authentication'''
from api.v1.auth.auth import Auth
import base64


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
