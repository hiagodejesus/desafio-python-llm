from pydantic import ValidationError
from flask import jsonify
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy.exc import SQLAlchemyError

from llm.prompt_chain import generate
from core.models import Classifications
from core.database import SessionLocal
from core.logger import get_logger

logger = get_logger(__name__, level="INFO")


def post_comments(data):    
    comments_list = data if isinstance(data, list) else [data]
    response_list = []
    
    # Criar uma nova sessão para cada execução
    session = SessionLocal()
    
    try:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(generate, comments_list))
            logger.info(f"Resultados obtidos: {results}")          
            
            for result in results:
                required_keys = {"categoria", "confianca", "tags_funcionalidades"}
                if isinstance(result, dict) and required_keys.issubset(result.keys()):
                    try:
                        classification = Classifications(
                            category=result["categoria"],
                            tags=result.get("tags_funcionalidades", []),
                            confidence=float(result["confianca"])
                        )
                        
                        logger.info(f"Criando classificação: category={classification.category}, confidence={classification.confidence}, tags={classification.tags}")
                        
                        session.add(classification)
                        session.flush()
                        
                        response_list.append({
                            "id": classification.id,
                            "categoria": classification.category,
                            "confianca": classification.confidence,
                            "tags_funcionalidades": classification.tags
                        })
                        
                        logger.info(f"Classificação adicionada à sessão com ID: {classification.id}")
                        
                    except ValueError as e:
                        logger.error(f"Erro de conversão de dados: {e}")
                        session.rollback()
                        return jsonify({"error": f"Erro de conversão: {str(e)}"}), 400
                        
                    except Exception as e:
                        logger.error(f"Erro ao criar classificação: {e}")
                        session.rollback()
                        return jsonify({"error": f"Erro ao criar classificação: {str(e)}"}), 400
                else:
                    logger.warning(f"Resultado inválido ou incompleto: {result}")
                    logger.warning(f"Chaves presentes: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            if response_list:
                session.commit()
                logger.info(f"Salvou {len(response_list)} classificações no banco de dados")
            else:
                logger.warning("Nenhuma classificação válida para salvar")
            
    except SQLAlchemyError as e:
        logger.error(f"Erro de banco de dados: {e}")
        session.rollback()
        return jsonify({"error": f"Erro de banco de dados: {str(e)}"}), 500
    
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        session.rollback()
        return jsonify({"error": f"Erro inesperado: {str(e)}"}), 500
    
    finally:
        session.close()
    
    logger.info(f"Response final: {response_list}")
    return jsonify({"classifications": response_list, "total": len(response_list)}), 200
