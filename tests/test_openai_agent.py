"""Mocked tests for the OpenAI integration layer.

These tests avoid real network calls by monkeypatching the client constructor.
"""
import os
import types
from openworld_tshm.agents.openai_agent import generate_with_openai


class _MockRespContent:
    def __init__(self, text: str):
        self.type = "output_text"
        self.text = text


class _MockRespMessage:
    def __init__(self, text: str):
        self.type = "message"
        self.content = [_MockRespContent(text)]


class _MockResponses:
    def __init__(self, text: str):
        self._text = text

    def create(self, **kwargs):  # pragma: no cover - simple
        return types.SimpleNamespace(output=[_MockRespMessage(self._text)], output_text=self._text)


class _MockChat:
    class _Completions:
        def create(self, **kwargs):
            msg = types.SimpleNamespace(content="fallback")
            choice = types.SimpleNamespace(message=msg)
            return types.SimpleNamespace(choices=[choice])

    def __init__(self):
        self.completions = _MockChat._Completions()


class _MockClient:
    def __init__(self, **kwargs):  # pragma: no cover - simple
        self.responses = _MockResponses("hello from agents")
        self.chat = _MockChat()


def test_generate_with_openai_agents(monkeypatch):
    # Ensure API key is set for the internal guard
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    # Monkeypatch client constructor inside our module
    def _fake_client():  # noqa: D401
        return _MockClient()

    monkeypatch.setattr("openworld_tshm.agents.openai_agent._get_client", _fake_client)
    text = generate_with_openai("prompt", model="gpt-test", use_agents=True)
    assert "hello from agents" in text


def test_generate_with_openai_chat_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test")

    # Client whose responses.create raises to trigger fallback
    class _BadResponses(_MockResponses):
        def create(self, **kwargs):
            raise RuntimeError("boom")

    class _Client(_MockClient):
        def __init__(self):
            super().__init__()
            self.responses = _BadResponses("")

    monkeypatch.setattr("openworld_tshm.agents.openai_agent._get_client", lambda: _Client())
    text = generate_with_openai("prompt", model="gpt-test", use_agents=True)
    assert text == "fallback"

