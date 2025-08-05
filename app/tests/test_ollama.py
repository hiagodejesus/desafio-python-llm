import os
import requests
from dotenv import load_dotenv
import pytest

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")


@pytest.mark.parametrize("prompt", ["Quais os generos musicais mais populares?"])
def test_generate(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )
    print("Status code:", response.status_code)
    print("Response:", response.text)

    assert response.status_code == 200, "response.status_code must be 200"
