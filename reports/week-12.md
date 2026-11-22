# Semester Week 12 Progress Report

## Completed Work

- I made fake data for courses, students, deadlines and teacher notes (`src/data.py`).
- I wrote four tools that read this data (`src/tools.py`): student courses, course info, deadlines and notes.
- I wrote checks for tool arguments and tool results (`src/validation.py`).
- I added structured output: the LLM writes a course summary as JSON and the program checks it, with one retry (`src/structured.py`).
- I added the commands `data` and `course` to `main.py`.
- I wrote 18 new tests. The project has 26 tests now and they all pass.
- I updated the proposal: a deadline has a date and a title, and I wrote this in the Change Notes.

## Important Commits

## Important Commits

- Commit hash: 4656c45
- Description: fake data, four tools, validation and structured output.
- Link: https://github.com/adiateraly/ai-agents-final-adiateraly/commit/4656c45

- Commit hash: a5d1f01
- Description: week 12 report, updated PROJECT.md and proposal.
- Link: https://github.com/adiateraly/ai-agents-final-adiateraly/commit/a5d1f01

- Commit hash: ba30078
- Description: stop tracking Python cache files (cleanup).
- Link: https://github.com/adiateraly/ai-agents-final-adiateraly/commit/ba30078

## Current Functionality

I can run `python main.py data S001` to see the fake data without an API key. I can run `python main.py course AI101` and the LLM gives a short summary as checked JSON. Wrong inputs (for example `ai 101; drop`) are rejected with a clear message. `python -m unittest` runs 26 tests.

## Problems Encountered

- The LLM does not always return clean JSON. Sometimes there is extra text around it.
- It was not clear how to check data coming from tools and from the model.
- I wanted tests that do not need an API key.

## Solutions

- I search for the first `{` and the last `}` in the answer, then read the JSON and check every field. If the check fails, I send the error back to the model and ask again (one retry). After that I stop with a clear error.
- I wrote one small function for each check (`check_course_id`, `is_valid_date`) and one table of rules for all tools.
- I made a fake model class (`ScriptedLLM`) for tests. It returns prepared answers.

## What I Learned

- What structured output is and why we validate it.
- Why we check inputs before using them (IDs, types, dates).
- Why tools should return an error object instead of crashing.
- How to test code that uses an LLM, with a fake model.
- AI help: I used an AI assistant (Claude) to write the first version of the code and the guide. I ran and tested the code and I am learning to explain every part.

## Next Week

- Give the tools to the LLM with tool descriptions (schemas).
- Let the LLM choose a tool, and run the real tool.
- Write a permission policy and a tool that saves a file with user approval.
- Add a trace of all tool calls.
