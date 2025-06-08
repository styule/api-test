import os
import pytest
from agenttest1.orchestrator import generate_post


@pytest.mark.asyncio
async def test_generate_post_contains_topic():
    api_key = os.getenv("OPENAI_API_KEY", "")
    # Skip if API key is missing, dummy, or obviously invalid (CI-safe)
    if (
        not api_key
        or api_key.lower().startswith("dummy")
        or "invalid" in api_key.lower()
    ):
        pytest.skip("No real OPENAI_API_KEY set; skipping OpenAI-dependent test.")
    topic = "why testing matters"
    post = await generate_post(topic)
    assert "testing" in post.lower()
    assert len(post) > 100  # Optional: ensure it's not empty or super short
