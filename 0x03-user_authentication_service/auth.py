#!/usr/bin/env python3
"""
this module takes a plain password
and hashes it
"""


import bcrypt


def _hash_password(password):
    """hashes and salts strings using bcrpt.hashpw"""
    pswd = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pswd, salt)
    return hashed_password
