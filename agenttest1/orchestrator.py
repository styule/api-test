import asyncio
from agenttest1.agents.researcher import ResearchAgent
from agenttest1.agents.writer import WriterAgent


async def generate_post(topic: str) -> str:
    researcher = ResearchAgent("researcher")
    writer = WriterAgent("writer")

    # Step 1: Researcher agent gathers notes
    research_notes = await researcher.run(topic)

    # Step 2: Writer agent turns notes into a blog post
    blog_post = await writer.run(research_notes)
    return blog_post


if __name__ == "__main__":
    import sys

    topic = sys.argv[1] if len(sys.argv) > 1 else "multi-agent systems"
    post = asyncio.run(generate_post(topic))
    print(post)


async def generate_post(topic: str) -> str:
    researcher = ResearchAgent("researcher")
    writer = WriterAgent("writer")

    research_notes = await researcher.run(topic)
    print("Researcher output:", research_notes)  # <-- ADD THIS

    blog_post = await writer.run(research_notes)
    print("Writer output:", blog_post)  # <-- ADD THIS
    return blog_post
