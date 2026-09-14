# Why use async and await when calling LLMs?

Run the same local language model through Ollama's synchronous and asynchronous Python clients. A pre-scheduled counter shows whether other work can proceed on the event loop while the application waits for a model response.

Start with `minimal_async.py`, the complete small program from the video. Then run `ollama_comparison.py` to see the counter experiment. This package is independent of Microsoft Agent Framework; the MAF call in the video is an API preview with agent setup omitted.

## Requirements

- Python 3.10 or newer. Tested with Python 3.13.7 on macOS.
- [Ollama](https://ollama.com/download), an application that runs language models locally. Install it and leave it running.
- The `qwen2:7b` model. Download it once with `ollama pull qwen2:7b`. The model requires several GB of storage and sufficient memory; it is not included here.
- The Ollama Python client, pinned in `requirements.txt` to the tested version 0.5.3.

## Run from this extracted folder

Create a virtual environment (an isolated set of Python packages):

```sh
python -m venv .venv
```

Activate it on macOS or Linux:

```sh
source .venv/bin/activate
```

On Windows PowerShell, use `.venv\Scripts\Activate.ps1` instead. Windows instructions are provided for convenience; the recorded execution used macOS.

```sh
python -m pip install -r requirements.txt
python minimal_async.py
python ollama_comparison.py
```

Both clients use Ollama's default local connection: `Client()` and `AsyncClient()`. No connection address is needed in the example. If you have previously set a custom `OLLAMA_HOST`, it overrides the default; use your intended local configuration.

## What to look for

The small program sends “Why is the sky blue?” and prints the answer.

The comparison sends “Explain why the sky is blue in five short sentences.” through both clients, using the same model, input, temperature, seed and output cap. It warms the model before the comparison.

In the recorded synchronous run, the counter remained at 0 during the 3.27-second request. In the asynchronous run, it displayed 1, 2 and 3 before the answer arrived at 3.18 seconds. See `Observed_Comparison.txt` for the actual captured output. Your timings, number of counter updates and answer can vary. The small timing difference is not evidence of faster model generation.

The synchronous call deliberately runs on the same event loop as the counter to demonstrate blocking. Both tasks share that loop. The counter is created with `asyncio.create_task(...)` before the model request; `await` does not create it. This is a learning comparison, not a production architecture or throughput benchmark.

## Try another question or model

Change the `content` string in `messages` in either file, for example to “Explain rainbows in two short sentences.” Keep both comparison calls using the same shared messages. To use another installed Ollama model, change `MODEL_NAME` to its exact name; download that model first if needed.

Keep `AsyncClient` together with `await`. Removing `await` from its `chat` call gives a coroutine object, not a completed answer. The working synchronous version uses `Client`. In a notebook that already runs an event loop, call `await main()` in a cell instead of `asyncio.run(main())`.

## Troubleshooting

- Connection error: make sure Ollama is installed and running, and check any custom environment configuration.
- Model not found: run `ollama pull qwen2:7b` or choose an installed model.
- No visible counter tick: a very fast reply may finish before the first second. Try a longer answer request; do not treat tick counts as a benchmark.
- Coroutine warning: restore the `await` on the asynchronous call.
- `asyncio.run()` cannot be called from a running event loop: run the file as a standalone script, or use the notebook guidance above.

## Sources

- [Ollama Python library](https://github.com/ollama/ollama-python)
- [Python coroutines and tasks](https://docs.python.org/3/library/asyncio-task.html)
- [Python runners](https://docs.python.org/3/library/asyncio-runner.html)
- [Microsoft Agent Framework: running agents](https://learn.microsoft.com/en-us/agent-framework/concepts/agents/running-agents)
- [FastAPI: concurrency and async / await](https://fastapi.tiangolo.com/async/)
