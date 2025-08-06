from flask import jsonify
from core.models import Classifications
from core.database import SessionLocal
from core.logger import get_logger

session = SessionLocal()

logger = get_logger(__name__, level="INFO")

def get_comments():
    try:
        comments = session.query(Classifications).all()
        comments_list = [{
            "category": comment.category,
            "tags": comment.tags,
            "confidence": comment.confidence,
        } for comment in comments]
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()
        logger.info(f"Comentários obtidos: {comments_list}")
        return jsonify(comments_list), 200