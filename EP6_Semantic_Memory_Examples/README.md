# Episode 6 — Simple semantic memory retrieval

Find two relevant memories, show the text sent to an answering model, and generate a short answer. The four facts are fictional practice data. This example accompanies **How Does an AI Find the Right Memory?**

Start with `semantic_memory.py`. It is the complete example: one Python file, four facts, one question, and two local models. It does not save new memories or change earlier episodes' data.

## Setup

Use Python 3.13 to match the tested setup. Install [Ollama](https://ollama.com/download) and keep it running. Ollama serves models on your computer; the Python program sends requests to it.

Download the two models once:

```bash
ollama pull nomic-embed-text
ollama pull qwen2:7b
```

`nomic-embed-text` creates embeddings, which are lists of numbers representing text. `qwen2:7b` writes the final answer. These are local models; this example needs no API key. Model downloads require an internet connection and several gigabytes of disk space.

Open a terminal in this extracted folder. Create a virtual environment, which keeps this example's Python packages together.

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python semantic_memory.py
```

Windows PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python semantic_memory.py
```

If PowerShell blocks activation, run `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.\.venv\Scripts\python.exe semantic_memory.py` instead. The Windows commands are supplied instructions; execution was checked on macOS.

## What happens

1. `retrieve_memories(question)` asks the embedding model to represent the question and four facts as numbers.
2. Python computes cosine similarity scores and sorts the facts by score.
3. `TOP_K = 2` keeps the two highest-scoring facts.
4. The selected **text**, together with the question, goes to a Microsoft Agent Framework agent.
5. The answering model produces a response using that supplied text.

The embedding model does not write the answer. The answering model does not receive the numeric vectors. Our Python code performs the ranking and selection; Microsoft Agent Framework runs the answering agent.

Nomic's `search_query:` and `search_document:` prefixes label the two kinds of embedding input. They are model-specific input instructions, not new memories. `cosine_similarity()` is a small calculation helper; you can follow the retrieval flow without learning its formula first.

## Expected behaviour

The default question is `What hobbies do I enjoy?` The live embedding check ranked gardening and reading first. Exact scores and generated answer wording may vary across model versions. The program prints all four scores, the exact user prompt passed to the answering agent, and its answer.

`OBSERVED_OUTPUT.txt` contains captured output from the complete runnable program. It is a reference, not a substitute for running the local models.

## Try another question

Edit this setting near the top of `semantic_memory.py`, save, and rerun the same command:

```python
QUESTION = "What is my favourite food?"
```

The four facts do not identify a favourite food. The retriever still selects two facts because this small example always takes the top two. The answering model is instructed to say that the saved memories do not contain the answer. This instruction is not a guaranteed validator.

Also try:

```python
QUESTION = "What is my occupation?"
```

The occupation fact should be retrieved. The second selected fact may be unrelated: `TOP_K` is a count, not proof that every selected item is useful. Each run starts a fresh answering agent, so previous answers do not reveal a missing fact.

Keep `TOP_K` at 2 for the video. You can later try 1 or 3. The script deliberately has no minimum-score threshold: similarity scores alone do not establish whether the answer exists. In particular, a score such as `0.75` does **not** mean a 75% chance that a fact answers the question.

## Scope and troubleshooting

- This is a tiny teaching example. It embeds all four memories on each run; it is not an efficient large-scale search system.
- The four strings stand in for previously saved memories. There is no database, automatic memory extraction, or persistence in this file.
- If Ollama cannot be reached, open the Ollama app or run `ollama serve` if you use the command-line server.
- If a model is missing, run the matching `ollama pull` command above. `ollama list` shows installed models.
- If imports fail, confirm that you activated the environment and installed `requirements.txt`. The listed package versions match this episode's tested Microsoft Agent Framework interface; the latest SDK may differ.
- The first request may take longer while a model loads. This is not a speed benchmark.

## Sources

- [Ollama embedding endpoint](https://docs.ollama.com/api/embed)
- [Nomic model card and task prefixes](https://huggingface.co/nomic-ai/nomic-embed-text-v1)
- [Microsoft Agent Framework: first agent](https://learn.microsoft.com/en-us/agent-framework/get-started/your-first-agent)
- [Retrieve-then-generate RAG](https://docs.langchain.com/oss/python/deepagents/retrieval)
