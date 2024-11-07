#!/usr/bin/env python3
'''Encrypt user set passwords'''
import bcrypt

def hash_password(password: str) -> bytes:
    '''function to encrypt password and return salted hashed password'''
    # salt password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
