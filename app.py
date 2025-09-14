# app.py
from flask import Flask, jsonify
from views.prompt_view import prompt_bp
from errors import register_error_handlers

def create_app():
    app = Flask(__name__)

    # Register routes/blueprints and error handlers
    app.register_blueprint(prompt_bp, url_prefix="/")
    register_error_handlers(app)

    # Health route MUST be inside create_app so tests see it
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok"}), 200

    return app

if __name__ == "__main__":
    # Local dev entrypoint: python app.py
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)

