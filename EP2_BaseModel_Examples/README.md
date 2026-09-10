# EP2 — How do you get structured answers from an LLM?

Download and unzip this folder. These are the Python examples from the episode, reorganized for learning and reuse. Both Python files are complete, independent examples with English comments.

| Start here | What you will do | What it needs |
| --- | --- | --- |
| `01_basemodel_basics.py` | Define `MemoryDecision`, parse JSON, read fields, inspect the schema, and try the validation examples | Python + Pydantic; no LLM |
| `02_llm_structured_output.py` | Pass `MemoryDecision` into an agent and use a real LLM answer in Python | Python + the packages below + a local Ollama model |

## 1. Set up Python

Use Python 3.10 or newer. Open a terminal **inside this extracted folder**, where `requirements.txt` is located.

Create a separate environment so the example's packages stay together.

**macOS / Linux**

```sh
python3 -m venv .venv
source .venv/bin/activate
```

**Windows Command Prompt**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

The commands below use `python` from this activated environment.

## 2. Try BaseModel first

```sh
python -m pip install pydantic==2.13.4
python 01_basemodel_basics.py
```

You will see `MemoryDecision` as the object type, `gardening` as a field value, and the JSON Schema. Two deliberately invalid inputs print validation errors; the program catches those errors and continues. A third example shows why a valid structure can still contain an incorrect meaning.

Every input in this first file is hand-written teaching data. It makes no model request. Once Pydantic is installed, it works offline.

## 3. Get a real answer from an LLM

Install the episode's packages:

```sh
python -m pip install -r requirements.txt
```

This example uses **Ollama**, an application that runs a language model on your computer. [Install Ollama](https://docs.ollama.com/quickstart), start it, and leave it running. Its local server should be available at `http://localhost:11434`.

Download the model used in EP2, then run the example:

```sh
ollama pull qwen2:7b
python 02_llm_structured_output.py
```

The model download is separate from this small code package, and generation speed depends on your computer. No API key is needed for this local example.

The default message is `I like gardening.` The program prints the actual JSON returned by the model, the `MemoryDecision` object type, its fields, and a simple application branch. See `example_output.txt` for a captured run; your model's wording or extracted values may differ.

## 4. Make it your own

Pass another message without editing the file:

```sh
python 02_llm_structured_output.py "I like painting."
```

You can also edit these clearly marked parts of `02_llm_structured_output.py`:

- `DEFAULT_MESSAGE`: the input used when no message is supplied.
- `MemoryDecision`: the fields and allowed values in your answer.
- `INSTRUCTIONS` and the `Field` description: what to extract and how to interpret it.
- `MODEL_NAME`: another locally installed model with compatible structured-output support.

If you change field names or allowed categories, update the extraction instructions, field access and application branch to match. Each example contains its own `MemoryDecision` definition so it can be copied independently.

## How this matches the video

```text
MemoryDecision(BaseModel)
          |
          v
Agent(default_options={"response_format": MemoryDecision, ...})
          |
          v
LLM returns JSON -> response.value -> decision.memory_value
```

`BaseModel` is Pydantic's base class, not the LLM. Defining a class alone does not send a model request. In the second example, the framework/client connects the schema to the request.

`Field(description=...)` adds guidance to the schema. It does not fill in a default value or check whether an answer is true. The first example demonstrates the difference: an unlisted category is rejected, while `skydiving` still passes the configured structural checks even though the message says `gardening`.

These examples print a proposed memory decision. They do not save anything to a database.

## If something does not run

- **Python or pip not found:** install Python, reopen the terminal, and activate the environment from step 1.
- **Module not found:** run the relevant install command in the same activated environment you use to run the file.
- **Cannot connect to Ollama:** start the Ollama app. If you installed its command-line server, run `ollama serve` in another terminal and leave it open.
- **Model not found:** run `ollama pull qwen2:7b`; `ollama list` shows locally installed models.
- **Timeout:** the first generation may need more time. Increase `TIMEOUT_SECONDS` in the second file if necessary.
- **An answer fails validation or has an unexpected meaning:** inspect the returned text and your instructions. Structural validation and extraction accuracy are separate concerns.

## Versions and references

The pinned top-level package versions match EP2. The examples were checked with Python 3.13.7; the declared minimum for these packages is Python 3.10. Windows and Linux execution were not separately tested.

- [Pydantic models and validation](https://docs.pydantic.dev/latest/concepts/models/)
- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)
- [Microsoft Agent Framework structured outputs](https://learn.microsoft.com/en-us/agent-framework/agents/structured-outputs)
- [Ollama setup](https://docs.ollama.com/quickstart)

Thanks for learning with me.
