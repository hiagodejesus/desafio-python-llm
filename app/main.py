from dotenv import load_dotenv
from flask import Flask, request, render_template

from core.wrapper import token_required
from core.database import SessionLocal, engine, Base
from core.logger import get_logger


from services.create import post_comments
from services.read import get_comments
from services.auth import jwt_login
from services.weekly_report import get_weekly_report


load_dotenv()

logger = get_logger(__name__, "INFO")

app = Flask(__name__)

Base.metadata.create_all(bind=engine)
session = SessionLocal()


@app.route('/comentarios', methods=['POST'])
@token_required
def create_comments():
    data = request.get_json()
    return post_comments(data)


@app.route('/comentarios', methods=['GET'])
@token_required
def read_comments():
    return get_comments()


@app.route('/relatorio/semana', methods=['GET'], endpoint='relatorio_semanal') 
def weekly_report():
    context = get_weekly_report()
    return render_template('weekly_report.html', graficos=context)


@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    return jwt_login(auth)


@app.route("/")
def index():
    return {
        "message": "Sistema de Classificação de Comentários",
        "endpoints": {
            "relatorio_semanal": "/login",
            "comentarios": "/comentarios",
            "relatorio_semanal": "/relatorio/semana",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
