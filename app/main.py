from dotenv import load_dotenv
from flask import Flask, request

from core.wrapper import token_required
from core.database import SessionLocal, engine, Base
from services.create import post_comments
from services.read import get_comments
from services.auth import jwt_login

load_dotenv()

app = Flask(__name__)

Base.metadata.create_all(bind=engine)
session = SessionLocal()


@app.route('/api/comentarios', methods=['POST'])
@token_required
def create_comments():
    data = request.get_json()
    return post_comments(data)


@app.route('/api/comentarios', methods=['GET'])
def read_comments():
    return get_comments()


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    return jwt_login(auth)


@app.route("/")
def index():
    return "Alumni API is running!"
