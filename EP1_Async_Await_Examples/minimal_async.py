"""The complete small async program shown during the syntax walkthrough."""

import asyncio
from ollama import AsyncClient

MODEL_NAME = "qwen2:7b"
messages = [{"role": "user", "content": "Why is the sky blue?"}]


async def main():
    client = AsyncClient()
    response = await client.chat(
        model=MODEL_NAME, messages=messages,
    )
    print(response.message.content)


if __name__ == "__main__":
    asyncio.run(main())
