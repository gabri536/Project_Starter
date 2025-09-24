import os
import httpx


SYSTEM = """You are a project-idea generator for beginners.
Avoid unsafe/illegal ideas. Return STRICT JSON only that matches the schema.
Be concrete; each idea must have 3–10 steps.
"""


class LLMClient:
    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.base = "https://api.openai.com/v1"

    async def json_chat(self, user: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": "gpt-4o-mini",
            "temperature": 0.3,
            "reponse_format": {"type": "json_object"},
            "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
        }
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(f"{self.base}/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            content = r.json()["choices"][0]["message"]["content"]
            if not isinstance(content, str):
                raise TypeError("Expected string content from OpenAI")
            return content
