import pytest

from example import ask_openai, client
from openai import OpenAIError


class DummyResponse:
    class Choice:
        def __init__(self, text: str):
            self.message = type("M", (), {"content": text})

    def __init__(self, text: str):
        self.choices = [DummyResponse.Choice(text)]


def test_ask_openai_success(monkeypatch):
    """ask_openai returns the assistant's reply on success."""
    # Monkey-patch client.chat.completions.create() to return our dummy
    monkeypatch.setattr(
        client.chat.completions,
        "create",
        lambda *, model, messages: DummyResponse("mock reply"),
    )
    assert ask_openai("hello") == "mock reply"


def test_ask_openai_error(monkeypatch):
    """ask_openai exits on API errors."""

    def raise_err(*, model: str, messages: list[dict[str, str]]):
        raise OpenAIError("boom")

    monkeypatch.setattr(
        client.chat.completions,
        "create",
        raise_err,
    )
    with pytest.raises(SystemExit):
        ask_openai("will error")
