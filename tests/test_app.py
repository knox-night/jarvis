from fastapi.testclient import TestClient

from jarvis.ai import providers
from jarvis.ai.providers import GeminiProvider
from jarvis.api import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_chat():
    response = client.post(
        "/chat",
        json={"message": "Hello JARVIS", "user_id": "test-user"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "response" in body
    assert body["provider"] in {"mock", "gemini"}
    assert isinstance(body["memory"], list)


def test_gemini_provider_uses_sdk(monkeypatch):
    calls = {}

    class FakeModels:
        def generate_content(self, **kwargs):
            calls.update(kwargs)

            class Response:
                text = "Gemini test response"

            return Response()

    class FakeClient:
        def __init__(self, api_key):
            calls["api_key"] = api_key
            self.models = FakeModels()

    monkeypatch.setattr(providers.genai, "Client", FakeClient)
    provider = GeminiProvider("test-key")

    result = provider.generate_response(
        "Hello",
        {"memory": ["User prefers concise answers"]},
    )

    assert result == "Gemini test response"
    assert calls["api_key"] == "test-key"
    assert calls["model"] == "gemini-3.6-flash"
    assert "Hello" in calls["contents"]
    assert "User prefers concise answers" in calls["contents"]
