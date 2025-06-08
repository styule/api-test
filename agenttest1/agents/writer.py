from .base import BaseAgent


class WriterAgent(BaseAgent):
    def run_prompt(self, notes: str) -> str:
        return (
            "You are a technical blog writer. "
            "Write a concise, engaging blog post for beginners, "
            "based only on these notes:\n"
            f"{notes}\n"
        )

    async def run(self, notes: str) -> str:
        prompt = self.run_prompt(notes)
        return await super().run(prompt)
