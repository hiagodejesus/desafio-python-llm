import requests

BASE_URL = "http://127.0.0.1:5000"

login_payload = {
    "username": "admin",
    "password": "admin"
}

login_response = requests.post(f"{BASE_URL}/login", json=login_payload)

if login_response.status_code != 200:
    logger.info("Erro ao autenticar:", login_payload)
    logger.info("Status code:", login_response.status_code)
    logger.info("Response text:", login_response.text)
    exit()

token = login_response.json()["token"]
logger.info("Token obtido:", token)
