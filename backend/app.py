from flask import Flask, jsonify
from flask_cors import CORS

from api.routes import api
from core.config import settings
from core.errors import register_error_handlers
from core.request_id import request_id_middleware


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": settings.cors_origins}})
    app.config["JSON_SORT_KEYS"] = False

    request_id_middleware(app)
    register_error_handlers(app)
    app.register_blueprint(api, url_prefix="/api")

    @app.get("/")
    def root():
        return jsonify({
            "name": "Jokor API",
            "status": "online",
            "version": settings.version,
            "docs": "/api/meta",
            "health": "/api/health",
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=settings.port, debug=settings.debug)
