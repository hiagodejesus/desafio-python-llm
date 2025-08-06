import re
import json
import requests
import requests

from typing import Any
from llm import OLLAMA_URL, MODEL_NAME
from core.logger import get_logger

logger = get_logger(__name__, level="INFO")


def query_ollama(prompt: str) -> dict[str, Any] | None:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "temperature": 0.0
        },
        timeout=300        
    )
    model_response =  response.json()["response"]
    json_response = json.loads(re.sub(r"```json|```", "", model_response).strip())
    logger.info(f"Resposta do modelo: {json_response}")
    return json_response
