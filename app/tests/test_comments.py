import pytest
import os

from app.main import app

USERNAME = os.getenv("JWT_USERNAME")
PASSWORD = os.getenv("JWT_PASSWORD")

COMMENTS = [
    {"id": 1, "texto": "Adorei a nova interface!"},
    {"id": 2, "texto": "Poderiam melhorar o desempenho."},
    {"id": 3, "texto": "Amei o novo recurso de playlist automática."},
    {"id": 4, "texto": "Não consigo acessar minha conta."},
    {"id": 5, "texto": "Interface limpa e fácil de usar."},
    {"id": 6, "texto": "Erro ao reproduzir faixas específicas."},
    {"id": 7, "texto": "Vocês vão adicionar suporte a letras de músicas?"},
    {"id": 8, "texto": "Aplicativo muito bom, parabéns!"},
    {"id": 9, "texto": "Por favor, incluam mais gêneros musicais."},
    {"id": 10, "texto": "SPAM SPAM SPAM SPAM SPAM"}
]

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def get_token(client):
    response = client.post("/login", json={"username": USERNAME, "password": PASSWORD})
    token = response.get_json()["token"]
    return token


@pytest.mark.parametrize("comments", COMMENTS)
def test_comments(client, comments):
    token = get_token(client)

    response = client.post(
        "/api/comentarios",
        json=comments,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200, f"Status code should be 200 instead of {response.status_code}"

    classifications = response.get_json()

    assert isinstance(classifications, list), f"Format should be List instead of {type(classifications)}"

    for item in classifications:
        assert set(item.keys()) == {"categoria", "confianca", "tags_funcionalidades"}, \
            'Expected keys {"categoria", "confianca", "tags_funcionalidades"}'
