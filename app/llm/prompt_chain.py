import requests
import urllib3
import requests

from typing import Any
from json import JSONDecodeError
from .ollama import query_ollama
from core.logger import get_logger
from llm import OLLAMA_URL, MODEL_NAME

logger = get_logger(__name__, level="INFO")


def generate(prompt: dict) -> dict[str, Any] | None:
    """Gera resposta do modelo via API do Ollama."""

    def classify_category(comment: str) -> dict[str, Any] | None:
        prompt = f"""
Você é um classificador de comentários.
Classifique o seguinte comentário **{comment}** em uma das categorias:
- ELOGIO, CRÍTICA, SUGESTÃO, DÚVIDA, SPAM, INDISPONÍVEL
**Formato de saída obrigatório (JSON)**
Exemplo: retornar apenas o seguinte JSON, **sem nenhuma explicação**:
{{
"categoria": "ELOGIO",
}}
"""
        return query_ollama(prompt)


    def classify_tags(comment: str) -> dict[str, Any] | None:
        prompt = f"""
Você é um classificador de comentários.
Classifique o seguinte comentário **{comment}** em uma das tags:
- feat_autotune, clip_narrativa, show_duração
**Formato de saída obrigatório (JSON)**
Exemplo: retornar apenas o seguinte JSON, **sem nenhuma explicação**:
{{
"tags_funcionalidades": [feat_autotune, clip_narrativa, show_duração]
}}
"""
        return query_ollama(prompt)


    def classify_confidence(comment: str, category: str, tags: list) -> dict[str, Any] | None:
        prompt = f"""
Você é um classificador de comentários.
Classifique o seguinte comentário **{comment}** em um intervalo de confiança de 0 a 1, onde 0 é nenhuma confiança e 1 é total confiança.:
{category} é categoria do comentário com as tags possíveis são: {tags} 
**Formato de saída obrigatório (JSON)**
Exemplo: retornar apenas o seguinte JSON, **sem nenhuma explicação**:
{{
"confianca": 0.0
}}
"""
        return query_ollama(prompt)

    if not OLLAMA_URL or not MODEL_NAME:
        raise ValueError("As variáveis de ambiente OLLAMA_URL e MODEL_NAME devem estar definidas.")
    if not isinstance(prompt, dict) or "texto" not in prompt:
        raise ValueError("O prompt deve ser um dicionário com a chave 'texto'.")
    
    try:
        category_response  = classify_category(prompt["texto"])
        tags_response  = classify_tags(prompt["texto"])

        category = category_response.get("categoria", "N/A")
        tags = tags_response.get("tags_funcionalidades", [])
    
        confidence_response  = classify_confidence(prompt["texto"], category, tags)
        classification = {
            "categoria": category,
            "confianca": confidence_response.get("confianca", 0.0),
            "tags_funcionalidades": tags 
        }
        logger.info(f"Classificação: {classification}")
        return classification
    except (urllib3.exceptions.ReadTimeoutError, requests.exceptions.ReadTimeout) as e:
        return {"message": "Tempo limite excedido", "error": str(e)}
    except (requests.exceptions.JSONDecodeError, JSONDecodeError) as e:
        return {"message": "Resposta inválida do modelo", "error": str(e)}
