import logging
from config import RAG_FILE, DEFAULT_RAG

logger = logging.getLogger(__name__)

def read_rag_query() -> str:
    try:
        return RAG_FILE.read_text(encoding="utf-8")
    except Exception as e:
        logger.error(f"Error reading RAG file: {e}. Using default")
        return DEFAULT_RAG

def save_rag_query(text: str):
    try:
        RAG_FILE.write_text(text, encoding="utf-8")
    except Exception as e:
        logger.error(f"Error saving RAG file: {e}")
        raise
