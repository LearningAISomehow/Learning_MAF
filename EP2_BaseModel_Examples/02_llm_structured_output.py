"""EP2: get a real structured answer from a local LLM.

Setup: python -m pip install -r requirements.txt
       Install/start Ollama, then run: ollama pull qwen2:7b
Run:   python 02_llm_structured_output.py
Try:   python 02_llm_structured_output.py "I like painting."

Ollama is the application running the LLM on your computer.
This local example needs no API key. It prints results without saving memories.
"""

import argparse
import asyncio
from typing import Literal

from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
from pydantic import BaseModel, Field, ValidationError


# Change these settings to use another locally installed, compatible model.
MODEL_NAME = "qwen2:7b"
OLLAMA_HOST = "http://localhost:11434"
DEFAULT_MESSAGE = "I like gardening."
TIMEOUT_SECONDS = 120


# Kept in this file so you can copy and use this example independently.
class MemoryDecision(BaseModel):
    memory_type: Literal["profile", "preference", "event", "none"]
    memory_key: str
    memory_value: str = Field(
        description=(
            "For a preference, extract only the activity or preference "
            "explicitly stated by the user. Do not add details."
        )
    )


INSTRUCTIONS = (
    "Extract one memory from the user's message. "
    "Use profile for a stable personal fact, preference for a like or dislike, "
    "event for a past experience, and none when there is no memory to extract. "
    "For a preference, use likes or dislikes as memory_key and the activity "
    "as memory_value. Only use information explicitly stated in the message. "
    "For none, use empty strings for memory_key and memory_value."
)


async def main(message: str) -> MemoryDecision:
    client = OllamaChatClient(model=MODEL_NAME, host=OLLAMA_HOST)

    # This is the connection highlighted in the video:
    # pass the MemoryDecision CLASS to response_format, not an instance.
    extractor = Agent(
        client=client,
        instructions=INSTRUCTIONS,
        default_options={"response_format": MemoryDecision, "temperature": 0},
    )

    print("Input:", message, flush=True)
    print("Calling local model:", MODEL_NAME, flush=True)
    response = await asyncio.wait_for(
        extractor.run(message), timeout=TIMEOUT_SECONDS
    )

    # response.text is the returned text; response.value is the parsed object.
    print("\nJSON text from the LLM:")
    print(response.text)
    decision = response.value
    if not isinstance(decision, MemoryDecision):
        raise ValueError("The response did not contain a MemoryDecision.")

    print("\nPython object:", type(decision).__name__)
    print("memory_type:", decision.memory_type)
    print("memory_key:", decision.memory_key)
    print("memory_value:", decision.memory_value)
    print("As a dictionary:", decision.model_dump())

    # Use the result in Python. This print statement does not store a memory.
    if decision.memory_type == "preference":
        print("Preference ready for application code:", decision.memory_value)
    else:
        print("No preference branch selected.")
    return decision


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message", nargs="?", default=DEFAULT_MESSAGE)
    args = parser.parse_args()
    try:
        asyncio.run(main(args.message))
    except asyncio.TimeoutError:
        raise SystemExit(
            "The local model timed out. Check that Ollama is running, or "
            "increase TIMEOUT_SECONDS if your computer needs longer."
        ) from None
    except ValidationError as error:
        raise SystemExit(f"The model's answer failed validation:\n{error}") from None
