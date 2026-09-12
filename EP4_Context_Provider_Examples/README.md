# EP4 — A Context Provider for SQLite memory

A small, runnable example of reading saved preferences before an agent answers, then extracting and saving useful new input afterwards. This is the full Python example shown in EP4, continuing EP3's manual memory loop.

Start with **provider_memory.py**. The database helpers, separate extractor, `SQLiteMemoryProvider`, agent registration and one-turn entry point are all in this file. The provider reads the same table format as the EP3 manual example when the database file and demo user identifier match.

## Set up

Use Python 3.13 (tested with 3.13.7). The dependencies are pinned in `requirements.txt` to the versions used for the video. This example was checked in that existing environment on macOS; the Windows commands below are setup guidance.

The example calls **Ollama**, an application that serves models locally. Install it from [ollama.com](https://ollama.com/), start the application, and download the model once:

```sh
ollama pull qwen2.5:7b
```

You need enough disk space and memory for that model. No API key is required by this example.

Open a terminal in this extracted example folder. Create a Python environment and install the dependencies:

macOS / Linux:

```sh
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python provider_memory.py
```

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe provider_memory.py
```

## Try the complete loop

At the bottom of `provider_memory.py`, edit the values passed to `run_example` and run the file again. Each launch starts a fresh conversation.

| Run | `user_message` | `save_new_memories` | Expected stored preferences |
| --- | --- | --- | --- |
| First launch | `I like gardening.` | `True` | gardening |
| Restart and recall | `What do I enjoy doing?` | `True` | gardening |
| Use an input without saving | `I like painting.` | `False` | gardening |
| Restart and recall | `What do I enjoy doing?` | `False` | gardening |
| Save the second preference | `I like painting.` | `True` | gardening, painting |
| Restart and recall both | `What do I enjoy doing?` | `True` | gardening, painting |

Keep `database_path` the same across this sequence. Use a new filename to begin with an empty store without deleting an existing database. The paths are relative to the folder where you run Python.

The first message should produce a saved gardening preference. In the recorded restart run, the answer was:

```text
[BEFORE] Loaded: ['gardening']
[RETURNED] You enjoy gardening.
[DATABASE] ['gardening']
```

`example_output.txt` contains the captured runs. Model wording and extraction decisions can vary. Use the printed database rows to check what actually persisted.

## What to change

- Change the message to test another positive activity preference. The demonstration's extraction and validation rules accept preferences under the `likes` key.
- Change the database filename for an independent experiment.
- Change `save_new_memories` to skip this provider's extraction/write path while continuing to read saved preferences.
- `USER_ID` selects the demo user's database rows. It is distinct from the provider's `source_id`, which labels its context contribution.
- If you change the schema or kind of memory, update `MemoryDecision`, the extractor instructions and `save_if_useful` together.

`after_run` completes after response generation but inside the non-streaming awaited `agent.run` call. The caller receives the response after those provider steps finish. The extractor agent does not have this memory provider attached.

## Scope and troubleshooting

This is a sequential, single-user teaching example. It loads all that user's positive preferences, performs no semantic search, and does not demonstrate production failure recovery. The extractor can make mistakes. The saving switch controls this preference store; other application logging needs separate controls.

- Connection refused: start Ollama and confirm it is running locally on port 11434.
- Model not found: run `ollama pull qwen2.5:7b`, then retry.
- Import error: use the environment where the pinned requirements were installed.
- Unexpected old preferences: confirm your current working folder and database filename; use a fresh filename for a clean test.
- An unexpected extraction: inspect `[EXTRACT]` and `[CHECK]`. A successful model call is not a guarantee that classification was correct.

## Sources

- [Microsoft Agent Framework — Context Providers](https://learn.microsoft.com/en-us/agent-framework/concepts/agents/conversations/context-providers)
- [Ollama](https://ollama.com/)

Package verification and video examples used agent-framework-core 1.15.0, agent-framework-ollama 1.0.0b260813, Pydantic 2.13.4 and ollama 0.5.3. These are the tested versions, not a claim about the newest release.
