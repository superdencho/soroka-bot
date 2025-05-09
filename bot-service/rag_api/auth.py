import os
import logging
from base64 import b64decode
from flask import request, Response

logger = logging.getLogger(__name__)

UI_USER = os.getenv("RAG_EDITOR_USERNAME", "")
UI_PASS = os.getenv("RAG_EDITOR_PASSWORD", "")

def check_ui_auth(header: str) -> bool:
    if not header or not header.startswith("Basic "):
        return False
    try:
        token = header.split(" ", 1)[1]
        user, pwd = b64decode(token).decode().split(":", 1)
    except Exception:
        return False
    return user == UI_USER and pwd == UI_PASS

def require_ui_auth(static_url_path: str):
    path = request.path
    if path.startswith(static_url_path) and not path.startswith("/api/"):
        auth = request.headers.get("Authorization", "")
        if not check_ui_auth(auth):
            return Response(
                "Authentication required",
                401,
                {"WWW-Authenticate": 'Basic realm="Restricted"'}
            )
