from flask import Blueprint, request, jsonify
from services.prompt_service import match_prompt, validate_payload
from errors import MissingDataError, InvalidTypeError, InvalidPromptError

prompt_bp = Blueprint("prompt", __name__)

@prompt_bp.route("match-prompt", methods=["POST"])
def match_prompt_view():
    payload = request.get_json(silent=True)
    if payload is None:
        # Malformed or non-JSON body
        return jsonify({"error": "Missing Data", "details": ["JSON body is required"]}), 400

    # Validate required fields + types
    try:
        validated = validate_payload(payload)
    except MissingDataError as e:
        return jsonify({"error": "Missing Data", "details": e.details}), 400
    except InvalidTypeError as e:
        return jsonify({"error": "Missing Data", "details": e.details}), 400

    # Try to match a prompt
    try:
        prompt_label = match_prompt(
            validated["situation"], validated["level"], validated["file_type"]
        )
        return jsonify({"prompt": prompt_label}), 200
    except InvalidPromptError as e:
        return jsonify({"error": "Invalid Prompt", "details": str(e)}), 422
