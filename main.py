import os
import jwt
from datetime import datetime, timedelta, timezone

from functools import wraps
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')

        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'message': 'Token ausente!'}), 401

        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user = payload
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido!'}), 401

        return f(*args, **kwargs)

    return decorated


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()

    if not auth or auth.get('username') != os.getenv("JWT_USERNAME") or auth.get('password') != os.getenv("JWT_PASSWORD"):
        return jsonify({'message': 'Credenciais inválidas'}), 401

    token = jwt.encode({
        'user': auth['username'],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})


@app.route('/ingest', methods=['POST'])
@token_required
def ingest():
    data = request.get_json()
    return jsonify({
        'message': 'Dados ingeridos com sucesso!',
        'usuario': request.user['user'],
        'data': data
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
