# EP3: Build a manual memory loop

Companion code for **How can an agent remember across conversations?**

This small example makes the complete order visible:

Read saved preferences → add context → answer → extract from the **new user input** → check → save an accepted preference. The next question reads the database again. A `none` decision skips the write.

## Setup

The captured run used Python 3.13.7 and the exact packages in `requirements.txt`. SQLite is included with Python. Install Ollama from its official site, https://ollama.com/, start the local service, and download the model:

```bash
ollama pull qwen2.5:7b
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`. Ollama must be running locally when you call the script. These are the versions used for this example, not a claim about the latest available SDK.

## 1. Compare one session with a restart

```bash
python manual_memory.py --history-only --message "I like gardening." --message "What do I enjoy doing?"
python manual_memory.py --history-only --message "What do I enjoy doing?"
```

The first command makes two calls using one session. The second command starts a fresh process. This script does not save or restore the session history; other applications can.

## 2. Follow the persistent memory loop

Choose a new database filename for an empty starting store. Run these commands in order from the same folder:

```bash
python manual_memory.py --database my_demo.db --message "I like gardening."
python manual_memory.py --database my_demo.db --message "What do I enjoy doing?"
python manual_memory.py --database my_demo.db --message "I like painting."
python manual_memory.py --database my_demo.db --message "What do I enjoy doing?"
```

Every command creates a new session while reusing the database file and fixed `demo_user`. The printed trace shows READ, CONTEXT, ANSWER, EXTRACT, CHECK, SAVE and DATABASE. A question normally produces `none` and does not add a row. The model's wording and classifications can vary across runs.

## How the Python fits together

- `MemoryDecision`: the extractor's structured result; creating it does not save anything.
- `read_preferences`: reads this user's values from SQLite.
- `build_messages`: puts saved preferences and the current input into the answering context.
- `run_with_memory`: explicitly runs the before-answer and after-answer work.
- `extract_memory`: makes a separate model call using only the original new user message.
- `save_if_useful`: checks the decision, normalises text, inserts an exact unique user/value pair and commits.

There are no custom ContextProvider hooks in this episode. The agent's tools are not making the read/save decisions; the Python application controls the sequence.

## Actual results and a limitation

`captured_demo.json` and `Sample_Output.txt` contain the executed results used in the video. The capture matches the included source hash. They are examples, not guaranteed wording.

The separate probe `I might try painting this weekend.` was incorrectly classified as a preference and saved to `edge_case.db`. This is explicitly shown in the video. Schema validity and a field-based saving rule do not independently establish truth or long-term usefulness.

To examine that boundary without mixing it into the main demo:

```bash
python manual_memory.py --database separate_edge_case.db --message "I might try painting this weekend."
```

The example loads all this user's positive activity preferences. It does not implement semantic relevance search, semantic deduplication, deletion, multi-user authentication, concurrent writes or production recovery. The fixed user identifier is a teaching simplification. Use a new filename to repeat the empty-store test without deleting existing work.
