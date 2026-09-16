from flask import Flask, jsonify
from flask_cors import CORS

from api.routes import api

app = Flask(__name__)
CORS(app)
app.register_blueprint(api, url_prefix="/api")


@app.get("/")
def root():
    return jsonify({
        "name": "Jokor API",
        "status": "online",
        "version": "0.1.0",
        "endpoints": ["/api/health", "/api/player/<region>/<uid>"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
