import logging
from flask import Blueprint, jsonify, request
from config import RAG_FILE, DEFAULT_RAG

logger = logging.getLogger(__name__)

bp = Blueprint("rag", __name__, url_prefix="/api")

@bp.route("/rag", methods=["GET"])
def get_rag():
    try:
        text = RAG_FILE.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Error reading RAG file: {e}. Using default.")
        text = DEFAULT_RAG
    return jsonify({"text": text})

@bp.route("/rag", methods=["POST"])
def update_rag():
    try:
        data = request.get_json(force=True)
        RAG_FILE.write_text(data["text"], encoding="utf-8")
        return jsonify({"status": "success"})
    except Exception as e:
        logger.error(f"Error saving RAG file: {e}")
        return jsonify({"error": str(e)}), 500

