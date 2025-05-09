from flask import Flask, send_from_directory
from flask_cors import CORS

from rag_api.routes import bp as rag_bp
from rag_api.auth import require_ui_auth

def create_app(
    static_folder: str = "static",
    static_url_path: str = "/",
) -> Flask:
    app = Flask(
        __name__,
        static_folder=static_folder,
        static_url_path=static_url_path,
    )
    CORS(app)

    # BasicAuth для UI
    app.before_request(lambda: require_ui_auth(static_url_path))

    # регистрируем API-Blueprint
    app.register_blueprint(rag_bp)

    # корневая страница
    @app.route("/", methods=["GET"])
    def index():
        return send_from_directory(app.static_folder, "index.html")

    return app
