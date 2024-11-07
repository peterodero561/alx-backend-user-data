#!/usr/bin/env python3
'''Encrypt user set passwords'''
import bcrypt

def hash_password(password: str) -> bytes:
    '''function to encrypt password and return salted hashed password'''
    # salt password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''function to validate the hashed password'''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
