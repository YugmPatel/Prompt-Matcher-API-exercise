import json
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def post(client, payload):
    return client.post(
        "/match-prompt",
        data=json.dumps(payload),
        content_type="application/json",
    )

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_missing_field(client):
    payload = {"situation": "Commercial Auto", "level": "Structure", "data": ""}
    res = post(client, payload)
    assert res.status_code == 400
    body = res.get_json()
    assert body["error"] == "Missing Data"

def test_invalid_type(client):
    payload = {"situation": 123, "level": "Structure", "file_type": "Summary Report", "data": ""}
    res = post(client, payload)
    assert res.status_code == 400
    assert res.get_json()["error"] == "Missing Data"

def test_prompt_1(client):
    payload = {"situation": "Commercial Auto", "level": "Structure", "file_type": "Summary Report", "data": ""}
    res = post(client, payload)
    assert res.status_code == 200
    assert res.get_json()["prompt"] == "Prompt 1"

def test_prompt_2(client):
    payload = {"situation": "General Liability", "level": "Summarize", "file_type": "Deposition", "data": ""}
    res = post(client, payload)
    assert res.status_code == 200
    assert res.get_json()["prompt"] == "Prompt 2"

def test_prompt_3(client):
    payload = {"situation": "Commercial Auto", "level": "Summarize", "file_type": "Summons", "data": ""}
    res = post(client, payload)
    assert res.status_code == 200
    assert res.get_json()["prompt"] == "Prompt 3"

def test_prompt_4(client):
    payload = {"situation": "Workers Compensation", "level": "Structure", "file_type": "Medical Records", "data": ""}
    res = post(client, payload)
    assert res.status_code == 200
    assert res.get_json()["prompt"] == "Prompt 4"

def test_prompt_5(client):
    payload = {"situation": "Workers Compensation", "level": "Summarize", "file_type": "Summons", "data": ""}
    res = post(client, payload)
    assert res.status_code == 200
    assert res.get_json()["prompt"] == "Prompt 5"

def test_invalid_prompt(client):
    payload = {"situation": "Commercial Auto", "level": "Structure", "file_type": "Deposition", "data": ""}
    res = post(client, payload)
    assert res.status_code == 422
    assert res.get_json()["error"] == "Invalid Prompt"
