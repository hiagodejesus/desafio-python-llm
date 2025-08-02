import requests

BASE_URL = "http://127.0.0.1:5000"

def test_login_and_ingest():
    login_payload = {
        "username": "admin",
        "password": "admin"
    }
    login_response = requests.post(f"{BASE_URL}/login", json=login_payload)
    assert login_response.status_code == 200

    token = login_response.json().get("token")
    assert token is not None

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    ingest_payload = {
        "mensagem": "Teste de ingestão via pytest"
    }
    ingest_response = requests.post(f"{BASE_URL}/ingest", json=ingest_payload, headers=headers)

    assert ingest_response.status_code == 200
    json_data = ingest_response.json()
    assert json_data.get("message") == "Dados ingeridos com sucesso!"
    assert json_data.get("usuario") == "admin"
    assert json_data.get("data") == ingest_payload
