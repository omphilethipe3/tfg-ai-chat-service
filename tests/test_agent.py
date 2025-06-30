import os
import pytest
from unittest.mock import MagicMock, patch
from src.ai_agent.agent import chat_with_openai, chat_with_fastmcp

@pytest.fixture(autouse=True)
def set_api_key(monkeypatch):
    monkeypatch.setenv("AGENT_API_KEY", "test")

def test_chat_with_openai_no_function(monkeypatch):
    fake_response = MagicMock()
    msg = MagicMock(content="hi there", function_call=None)
    fake_response.choices = [MagicMock(message=msg)]
    monkeypatch.setattr("src.ai_agent.agent.openai_client.chat.completions.create",lambda **kw: fake_response)
    assert chat_with_openai("hello") == "hi there"


def test_chat_with_fastmcp(monkeypatch):
    fake = MagicMock()
    fake.chat.return_value = "ok"
    monkeypatch.setattr("src.ai_agent.agent.fastmcp.Agent", lambda **kw: fake)
    assert chat_with_fastmcp("test") == "ok"