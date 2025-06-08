import asyncio
from agenttest1.agentcore import Agent


class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.core = Agent()

    async def run(self, prompt: str) -> str:
        # Run the core Agent's logic in a thread to stay async-friendly
        return await asyncio.to_thread(self.core.run, prompt)
