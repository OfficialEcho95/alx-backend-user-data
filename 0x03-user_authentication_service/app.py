#!/usr/bin/env python3
"""
the flask app
"""
from flask import Flask, request, jsonify
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/')
def welcome():
    """the welcome route"""
    message = {"message": "Bienvenue"}
    return jsonify(message)


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """the endpoint to register users"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
