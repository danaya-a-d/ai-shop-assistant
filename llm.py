import asyncio
import os
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
from groq import AsyncGroq


load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


async def ask_llm(question: str) -> str:
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set")

    async with AsyncGroq(api_key=GROQ_API_KEY) as client:
        response = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            reasoning_effort="low",
            max_completion_tokens=300
        )

    return response.choices[0].message.content or "Пустой ответ"


async def main():
    answer = await ask_llm(
        "Сколько стоят наушники X1?"
    )
    print(answer)


if __name__ == "__main__":
    asyncio.run(main())
