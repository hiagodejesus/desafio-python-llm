import os
import time
import json
import requests
import urllib3
import requests

from typing import Any
from dotenv import load_dotenv
from json import JSONDecodeError

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

SYSTEM_PROMPT = """
Analise o seguinte comentário de um usuário e classifique-o com base nos critérios abaixo.

Comentário:
"{comentario}"

Responda no formato JSON com os seguintes campos:

- **categoria**: uma das opções — "ELOGIO", "CRÍTICA", "SUGESTÃO", "DÚVIDA", "SPAM" ou "INDISPONÍVEL"
- **tags_funcionalidades**: uma lista com zero ou mais das seguintes tags relacionadas ao comentário — "feat_autotune", "clip_narrativa", "show_duração"
- **confianca**: um número decimal entre 0.0 e 1.0 que indica o grau de certeza da classificação

Exemplo de resposta esperada:
```json
  "categoria": "ELOGIO",
  "tags_funcionalidades": ["feat_autotune", "clip_narrativa"],
  "confianca": 0.85
```
"""

def generate(prompt: dict) -> dict[str, Any] | None:
    """Gera resposta do modelo via API do Ollama."""

    if not OLLAMA_URL or not MODEL_NAME:
        raise ValueError("As variáveis de ambiente OLLAMA_URL e MODEL_NAME devem estar definidas.")
    if not isinstance(prompt, dict) or "texto" not in prompt:
        raise ValueError("O prompt deve ser um dicionário com a chave 'texto'.")

    full_prompt = SYSTEM_PROMPT.format(comentario=prompt["texto"])

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False
            },
            timeout=300        
        )
        if response.status_code == 200:
            json_response = response.json()
            print("json_response:", json_response["response"])
            return json.loads(json_response["response"])
        else:
            return {
                "error": f"Erro ao chamar o modelo. Status {response.status_code}",
                "response": response.text
            }

    except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
        return {"message": "Tempo limite excedido", "error": str(e)}
    except (requests.exceptions.JSONDecodeError, JSONDecodeError) as e:
        return {"message": "Resposta inválida do modelo", "error": str(e)}
