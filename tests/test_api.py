from fastapi.testclient import TestClient
import pytest
from src.api.main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_agents(monkeypatch):
    monkeypatch.setattr("src.api.main.chat_with_fastmcp", lambda msg: "fast-response")
    monkeypatch.setattr("src.api.main.chat_with_openai", lambda msg: "openai-response")

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json() == {"status": "ok"}

def test_chat_default_fastmcp():
    r = client.post("/chat", json={"message": "hey"})
    assert r.status_code == 200 and r.json() == {"response": "fast-response"}

def test_chat_openai():
    r = client.post("/chat", json={"message": "hey", "provider": "openai"})
    assert r.status_code == 200 and r.json() == {"response": "openai-response"}

def test_bad_request():
    r = client.post("/chat", json={"provider": "fastmcp"})
    assert r.status_code == 400 and "`message` is required" in r.json()["detail"]