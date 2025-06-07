# tests/test_example.py
import pytest

from example import ask_openai, client


class DummyResponse:
    """Mock OpenAI response object with a single choice."""

    class Choice:
        def __init__(self, content):
            # emulate the `.message.content` structure
            self.message = type("M", (), {"content": content})

    def __init__(self, content):
        self.choices = [DummyResponse.Choice(content)]


def test_ask_openai_success(monkeypatch):
    """ask_openai returns the assistant’s reply on success."""
    monkeypatch.setattr(
        client.chat.completions,
        "create",
        lambda **kwargs: DummyResponse("mock reply"),
    )
    assert ask_openai("hello") == "mock reply"


def test_ask_openai_error(monkeypatch):
    """ask_openai calls sys.exit on API errors."""
    from openai import OpenAIError

    def raise_error(**kwargs):
        raise OpenAIError("boom")

    monkeypatch.setattr(
        client.chat.completions,
        "create",
        raise_error,
    )
    with pytest.raises(SystemExit):
        ask_openai("this will error")
