import requests

BASE_URL = "http://127.0.0.1:5000"

login_payload = {
    "username": "admin",
    "password": "admin"
}

login_response = requests.post(f"{BASE_URL}/login", json=login_payload)

if login_response.status_code != 200:
    print("Erro ao autenticar:", login_response.json())
    exit()

token = login_response.json()["token"]
print("Token obtido:", token)

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

ingest_payload = {
    "mensagem": "Dados enviados com sucesso!",
    "origem": "script Python"
}

ingest_response = requests.post(f"{BASE_URL}/ingest", json=ingest_payload, headers=headers)

if login_response.status_code != 200:
    print("Erro ao autenticar:")
    print("Status code:", login_response.status_code)
    print("Response text:", login_response.text)
    exit()
else:
    print("Resposta do servidor:")
    print(ingest_response.json())
