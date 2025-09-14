from errors import InvalidPromptError, MissingDataError, InvalidTypeError

# Mapping rules: normalized to lowercase tuples
RULES = {
    ("commercial auto", "structure", "summary report"): "Prompt 1",
    ("general liability", "summarize", "deposition"): "Prompt 2",
    ("commercial auto", "summarize", "summons"): "Prompt 3",
    ("workers compensation", "structure", "medical records"): "Prompt 4",
    ("workers compensation", "summarize", "summons"): "Prompt 5",
}

REQUIRED_FIELDS = ["situation", "level", "file_type", "data"]

def _normalize(value):
    # Accept only strings, strip whitespace, lowercase for matching
    if not isinstance(value, str):
        raise InvalidTypeError([f"Value must be a string, got {type(value).__name__}"])
    return value.strip()

def validate_payload(payload: dict) -> dict:
    # Check presence
    missing = [f"'{f}' is required" for f in REQUIRED_FIELDS if f not in payload]
    if missing:
        raise MissingDataError(missing)

    # Type checks + normalization
    try:
        situation = _normalize(payload["situation"])
        level = _normalize(payload["level"])
        file_type = _normalize(payload["file_type"])
        # 'data' can be empty string but must be present and a string
        _ = _normalize(payload["data"])
    except InvalidTypeError as e:
        # Re-raise to be handled by view
        raise e

    return {
        "situation": situation,
        "level": level,
        "file_type": file_type,
        "data": payload["data"],  # keep original (may be empty)
    }

def match_prompt(situation: str, level: str, file_type: str) -> str:
    key = (situation.lower(), level.lower(), file_type.lower())
    prompt = RULES.get(key)
    if not prompt:
        raise InvalidPromptError("No prompt matches the provided filters.")
    return prompt
