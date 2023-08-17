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

    def create_session(self, email: str) -> str:
        """create and store user sessions"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user = self._db.add_user(email, session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """searches session id and returns the user"""
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
            return user

    def destroy_session(self, user_id: int) -> None:
        """destroys the user's session"""
        if user_id is None:
            return None
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """update user reset token"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError('User not found')
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(reset_token: str, password: str) -> None:
        """updates the user password"""
        user = None
        try:
            user = self._db.find_user_by(reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("user not found")
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)
