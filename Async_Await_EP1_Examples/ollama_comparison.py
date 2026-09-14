"""Compare a real synchronous and asynchronous call to the same local model.

The counter is an asyncio task on the SAME event loop in both cases.
Calling the synchronous client here deliberately demonstrates blocking that loop.
This is an explanation of responsiveness, not a model-speed benchmark.
"""

import asyncio
from time import perf_counter

from ollama import AsyncClient, Client


MODEL_NAME = "qwen2:7b"
messages = [{"role": "user", "content": "Explain why the sky is blue in five short sentences."}]
OPTIONS = {"temperature": 0, "seed": 7, "num_predict": 180}


def ask_sync():
    client = Client()
    response = client.chat(
        model=MODEL_NAME,
        messages=messages,
        options=OPTIONS,
        stream=False,
    )
    return response.message.content


async def ask_async():
    client = AsyncClient()
    response = await client.chat(
        model=MODEL_NAME,
        messages=messages,
        options=OPTIONS,
        stream=False,
    )
    return response.message.content


async def show_counter(done, started):
    count = 0
    while not done.is_set():
        print(f"{perf_counter() - started:5.2f}s  Waiting counter: {count}", flush=True)
        count += 1
        await asyncio.sleep(1)


async def demonstrate(label, asynchronous):
    print(f"\n{label}", flush=True)
    done = asyncio.Event()
    started = perf_counter()
    counter = asyncio.create_task(show_counter(done, started))
    # Let the counter display its initial zero before the model request.
    await asyncio.sleep(0)
    try:
        print(f"{perf_counter() - started:5.2f}s  Model request sent", flush=True)
        if asynchronous:
            answer = await ask_async()
        else:
            answer = ask_sync()
        print(f"{perf_counter() - started:5.2f}s  Model answer received", flush=True)
        print(answer, flush=True)
    finally:
        done.set()
        await counter


async def main():
    # Warm the same model before BOTH examples; no model downloads are performed.
    print("Preparing local model...", flush=True)
    await AsyncClient().chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": "Say ready."}],
        options={"num_predict": 2},
        keep_alive="5m",
    )
    await demonstrate("SYNCHRONOUS CLIENT", asynchronous=False)
    await demonstrate("ASYNCHRONOUS CLIENT + AWAIT", asynchronous=True)


if __name__ == "__main__":
    asyncio.run(main())
