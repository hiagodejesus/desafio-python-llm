import os
import pytest

from app.main import app
from dotenv import load_dotenv
from core.logger import get_logger

logger = get_logger(__name__, level="INFO")

load_dotenv()


COMMENTS = [
    {"id": 1, "texto": "Adorei a nova interface! Muito mais intuitiva"},
    {"id": 2, "texto": "O player trava quando tento mudar de faixa rapidamente."},
    {"id": 3, "texto": "Seria ótimo se tivesse um modo offline para playlists."},
    {"id": 4, "texto": "A qualidade do som está incrível depois da última atualização."}
]

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    response = client.post("/login", json={"username": os.getenv("JWT_USERNAME"), "password":  os.getenv("JWT_PASSWORD")})
    token = response.get_json()["token"]
    return token


@pytest.mark.parametrize("comments", COMMENTS)
def test_post_comments(client, comments):
    token = get_token(client)
    logger.info(f"Token: {token}")

    response = client.post(
        "/api/comentarios",
        json=comments,
        headers={"Authorization": f"Bearer {token}"}
    )

    logger.info(f"Response: {response.text}")
    assert response.status_code == 200, f"Status code should be 200 instead of {response.status_code}"

    classifications = response.get_json()
    logger.info(f"Classifications: {classifications}")

    assert isinstance(classifications, list), f"Format should be List instead of {type(classifications)}"

    for item in classifications:
        assert set(item.keys()) == {"categoria", "confianca", "tags_funcionalidades"}, \
            'Expected keys {"categoria", "confianca", "tags_funcionalidades"}'


def test_get_comments(client):
    response = client.get("/api/comentarios")
    logger.info(f"Response: {response.text}")

    assert response.status_code == 200, f"Status code should be 200 instead of {response.status_code}"

    comments = response.get_json()
    logger.info(f"Comments: {comments}")

    assert isinstance(comments, list), f"Format should be List instead of {type(comments)}"

    for comment in comments:
        assert set(comment.keys()) == {"category", "confidence", "tags"}, \
            'Expected keys {"category", "confidence", "tags"}'
