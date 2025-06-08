from agenttest1.tools import get_time, reverse_text
from agenttest1.tools import calculator


def test_get_time():
    result = get_time()
    assert "time" in result
    assert isinstance(result["time"], str)


def test_reverse_text():
    result = reverse_text("hello")
    assert result["reversed"] == "olleh"
    assert isinstance(result["reversed"], str)


def test_calculator():
    assert calculator("2 + 2")["result"] == 4.0
    assert calculator("3 * (5 + 1)")["result"] == 18.0
    assert "error" in calculator("invalid input")
