import os
import jwt
import datetime

from pydantic import ValidationError
from flask import jsonify
from core.types import Credentials


def jwt_login(auth):
    try:
        credentials = Credentials(**auth)
    except ValidationError:
        return jsonify({'message': 'Invalid credentials'}), 400

    if credentials.username != os.getenv("JWT_USERNAME") or credentials.password != os.getenv("JWT_PASSWORD"):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user': auth['username'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }, os.getenv('JWT_SECRET_KEY'), algorithm="HS256")

    return jsonify({'access_token': token})
