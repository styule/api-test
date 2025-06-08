import pytest
from agenttest1.orchestrator import generate_post


@pytest.mark.asyncio
async def test_generate_post_contains_topic():
    topic = "why testing matters"
    post = await generate_post(topic)
    # Make sure the core subject of the topic appears in the post
    assert "testing" in post.lower()
    assert len(post) > 100  # Optional: ensure it's not empty or super short
