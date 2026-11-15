# Academic Planner Agent

An AI helper for university students. It answers questions about courses and deadlines.
Project for CSS 4007. Level A (autonomous agent).

## What works now (week 11)

- The program sends a question to an LLM (OpenAI API) and prints the answer.
- Errors are handled: missing key, wrong key, wrong model, no internet, bad API answer.
- 8 automatic tests with a fake API.

## What you need

- Python 3.10 or newer
- An OpenAI API key (platform.openai.com)
- No extra packages. The program uses only the standard Python library.

## Setup

1. Copy `.env.example` to a new file named `.env`.
2. Open `.env` and write your values:

   ```text
   LLM_API_KEY=your-secret-key
   LLM_MODEL=your-model-name
   ```

3. The `.env` file is ignored by Git, so your key stays on your computer.

## Run

```text
python main.py "Say hello in one short sentence."
```

You can also run `python main.py` and type your question when the program asks.

## Run the tests

```text
python -m unittest -v
```

The tests use a fake API. They need no key and no internet.

## Files

| File | What it does |
|---|---|
| `main.py` | Starts the program and prints the answer |
| `src/model_client.py` | Sends the request to the LLM and handles errors |
| `tests/test_model_client.py` | Automatic tests |
| `.env.example` | Example settings (no secrets) |
| `reports/` | Proposal and weekly reports |

## AI assistance

An AI assistant (Claude) helped to write this code.
