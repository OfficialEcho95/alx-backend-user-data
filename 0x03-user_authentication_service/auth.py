#!/usr/bin/env python3
"""
this module takes a plain password
and hashes it
"""


import bcrypt
import uuid
from uuid import uuid4
from db import DB
from user import User
from user import Base
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hashes and salts strings using bcrpt.hashpw"""
    pswd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pswd, salt)
    return hashed_password


def _generate_uuid() -> str:
    """uuid generator"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """the register method"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user
        raise ValueError("User {} already exists.".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """validating that a user exists and can log in"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        return bcrypt.checkpw(password.encode('utf-8'), user_password)
