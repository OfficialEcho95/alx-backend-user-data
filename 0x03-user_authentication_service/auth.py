#!/usr/bin/env python3
"""
this module takes a plain password
and hashes it
"""


import bcrypt
from db import DB
from user import User
from user import Base


def _hash_password(password: str) -> bytes:
    """hashes and salts strings using bcrpt.hashpw"""
    pswd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pswd, salt)
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """the register method"""
        if self._db.find_user_by(email=email):
            raise ValueError("User {} already exists.".format(email))
        else:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
