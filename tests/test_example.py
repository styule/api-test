# tests/test_example.py

import pytest

from example import ask_openai, client


class DummyResponse:
    """Mimic the shape of an OpenAI ChatCompletion response."""

    class Choice:
        def __init__(self, content: str) -> None:
            self.message = type("M", (), {"content": content})

    def __init__(self, content: str) -> None:
        self.choices = [DummyResponse.Choice(content)]


def test_ask_openai_success(monkeypatch):
    """ask_openai returns the assistant’s reply on success."""
    monkeypatch.setattr(
        client.chat.completions,
        "create",
        lambda *_, **__: DummyResponse("mock reply"),
    )
    assert ask_openai("hello") == "mock reply"


def test_ask_openai_error(monkeypatch):
    """ask_openai exits with SystemExit on API errors."""
    from openai import OpenAIError

    def raise_err(*_: object, **__: object) -> None:
        raise OpenAIError("boom")

    monkeypatch.setattr(
        client.chat.completions,
        "create",
        raise_err,
    )
    with pytest.raises(SystemExit):
        ask_openai("will error")
