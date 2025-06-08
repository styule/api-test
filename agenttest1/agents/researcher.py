from .base import BaseAgent


class ResearchAgent(BaseAgent):
    def run_prompt(self, topic: str) -> str:
        return (
            f"You are an expert researcher. "
            f"List 5–7 key facts, statistics, or insights about this topic:\n"
            f"{topic}\n"
            f"Give the facts only, no introduction."
        )

    async def run(self, topic: str) -> str:
        prompt = self.run_prompt(topic)
        return await super().run(prompt)
