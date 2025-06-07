import pytest
from example import ask_openai, client

class DummyResponse:
    class Choice:
        def __init__(self, text):
            self.message = type("M", (), {"content": text})

    def __init__(self, text):
        self.choices = [DummyResponse.Choice(text)]

def test_ask_openai_success(monkeypatch):
    """ask_openai returns the assistant's reply when the API call succeeds."""
    monkeypatch.setattr(
        client.chat.completions,
        "create",
        lambda model, messages: DummyResponse("mock reply")
    )
    result = ask_openai("hello")
    assert result == "mock reply"

def test_ask_openai_error(monkeypatch):
    """ask_openai exits on API errors."""
    from openai import OpenAIError

    def raise_err(model, messages):
        raise OpenAIError("boom")

    monkeypatch.setattr(
        client.chat.completions,
        "create",
        raise_err
    )
    with pytest.raises(SystemExit):
        ask_openai("will error")
