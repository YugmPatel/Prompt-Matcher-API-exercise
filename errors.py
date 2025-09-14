from flask import jsonify

class MissingDataError(Exception):
    def __init__(self, details):
        super().__init__("Missing Data")
        self.details = details if isinstance(details, list) else [str(details)]

class InvalidTypeError(Exception):
    def __init__(self, details):
        super().__init__("Invalid Type")
        self.details = details if isinstance(details, list) else [str(details)]

class InvalidPromptError(Exception):
    pass

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_):
        return jsonify({"error": "Method Not Allowed"}), 405

    @app.errorhandler(500)
    def internal_error(_):
        # Do not leak internals
        return jsonify({"error": "Internal Server Error"}), 500
