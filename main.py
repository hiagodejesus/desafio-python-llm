import os
from typing import TypedDict

import jwt
import datetime
from functools import wraps
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from concurrent.futures import ThreadPoolExecutor

from llm.ollama import generate

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")


class Comments(BaseModel):
    id: int
    texto: str

    class Config:
        extra = "forbid"


class Credentials(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"


class LoginResponse(TypedDict):
    message: str


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/api/comentarios', methods=['POST'])
@token_required
def comments():
    data = request.get_json()
    comments_list = data if isinstance(data, list) else [data]

    try:
        is_valid = all(Comments(**item) for item in comments_list)
    except ValidationError:
        is_valid = False

    if is_valid:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(generate, comments_list))
            print(results)
            return jsonify(results)
    return jsonify({"error": "Invalid or empty JSON"}), 400


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    try:
        credentials = Credentials(**auth)
    except ValidationError:
        return jsonify({'message': 'Invalid credentials'}), 400

    if credentials.username != os.getenv("JWT_USERNAME") or credentials.password != os.getenv("JWT_PASSWORD"):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = jwt.encode({
        'user': auth['username'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})


if __name__ == '__main__':
    app.run(debug=False)
