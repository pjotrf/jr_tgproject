from openai import AsyncOpenAI
from config import OPENAI_API_KEY

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

DEFAULT_MODEL = "gpt-4o-mini"

async def ask_gpt(prompt: str, temperature: float = 1.0, model: str = DEFAULT_MODEL) -> str:

    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        return f"⚠ Ошибка GPT: {e}"
