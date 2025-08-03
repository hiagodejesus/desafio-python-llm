import os
import json
import requests

from typing import List, Any
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from json import JSONDecodeError

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")

SYSTEM_PROMPT = """
Você é um classificador de comentários de usuários sobre um aplicativo de música.

Seu objetivo é analisar o comentário fornecido e retornar um JSON com a seguinte estrutura:

{{
  "categoria": string,                      # Pode ser: "ELOGIO", "CRÍTICA", "SUGESTÃO", "DÚVIDA", "SPAM" ou "INDISPONÍVEL"
  "tags_funcionalidades": list[str],       # Lista de funcionalidades mencionadas, como "feat_autotune", "clip_narrativa", "show_duração", etc.
  "confianca": float                        # Um valor de 0.0 a 1.0 indicando a confiança da classificação
}}

Atenção:
- Não adicione explicações ou comentários extras.
- Responda **apenas** com o JSON.
- Use "INDISPONÍVEL" se não conseguir classificar o comentário.
- A chave "confianca" deve ser um número decimal entre 0.0 e 1.0.

Exemplo de entrada:

Comentário: "Gostei muito da nova interface, está bem mais rápida!"

Saída esperada:
{{
  "categoria": "ELOGIO",
  "tags_funcionalidades": [],
  "confianca": 0.92
}}

Agora classifique o seguinte comentário:

{comentario}
"""



class LLMResponse(BaseModel):
    categoria: str
    tags_funcionalidades: List
    confianca: float


def generate(prompt: dict) -> dict[str, Any] | None | Any:
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma:2b",
            "prompt": SYSTEM_PROMPT.format(comentario=prompt.get("texto", "Sem comentários")),
            "stream": False
        }
    )

    mock_response = {"categoria": "", "tags_funcionalidades": [], "confianca": 0.0}

    if response.status_code == 200 and hasattr(response, "json"):
        model_response = response.json().get("response")
        try:
            json_response = json.loads(model_response)
            LLMResponse.model_validate(json_response)
            return json_response
        except (JSONDecodeError, ValidationError):
            pass
    return mock_response
