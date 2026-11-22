# Academic Planner Agent

An AI agent for university students. It answers questions about courses and deadlines and builds a study plan.
Project for CSS 4007. Level A (autonomous agent).

## What works now (week 12)

- The program sends a question to an LLM (OpenAI API) and prints the answer. Errors are handled (no key, wrong key, wrong model, no internet, bad answer).
- Fake data and four read-only tools (student courses, course info, deadlines, notes). Arguments and results are checked. The LLM can return a checked JSON summary of a course.

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
python main.py "Say hello in one short sentence."   # ask the LLM
python main.py course AI101                          # LLM summary as checked JSON
python main.py data S001                             # show the fake data (no key needed)
```

## Run the tests

```text
python -m unittest -v
```

The tests use a fake model and need no key and no internet.

## Files

| File | What it does |
|---|---|
| `main.py` | Command line |
| `src/model_client.py` | Sends requests to the LLM, handles API errors |
| `src/data.py` | Fake data |
| `src/tools.py` | The tools |
| `src/validation.py` | Checks for tool arguments and results |
| `src/structured.py` | Checked JSON from the LLM |
| `tests/` | Automatic tests |
| `reports/` | Proposal, weekly reports, final report |

## AI assistance

An AI assistant (Claude) helped to write the code, the tests and the documents. I ran and tested the code, and I am responsible for understanding and explaining it.
