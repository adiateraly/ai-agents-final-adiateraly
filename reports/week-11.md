# Semester Week 11 Progress Report

## Completed Work

- I opened the project folder in VS Code.
- The `.env` file is ignored by Git, so the key is not uploaded.
- I wrote `src/model_client.py`. The function `complete(messages, tools)` sends a request to the LLM API and returns the text and the tool calls.
- I added error handling: missing key, wrong key, wrong model name, no internet, and bad API answers. Temporary errors are tried again two times.
- I wrote `main.py`. It sends a question to the LLM and prints the answer.
- I wrote 8 automatic tests with a fake API and a short setup guide in `PROJECT.md`.
- I decided to build level A instead of level C. I updated `reports/proposal.md` (new tools, state, guardrails, 12 tests, paper) and wrote the change in its "Change Notes" section.

## Important Commits

- Commit hash: a07eebb
- Description: model client, first working request and tests.
- Link: https://github.com/ardakshalkar/css4007-ai-agents-final/commit/a07eebb475af1f48c554134ee9848803b0c3588f

- Commit hash: b39da6a
- Description: final project files, setup guide and week 11 report.
- Link: https://github.com/ardakshalkar/css4007-ai-agents-final/commit/b39da6acf0dbe6395e4c0408bf20a2a1013c6143

## Current Functionality

I can run `python main.py "Say hello"` and the LLM answers in the terminal. If something is wrong (no key, no internet, wrong model), the program shows a clear message and does not crash. The command `python -m unittest -v` runs 8 tests and they pass.

## Problems Encountered

- The program must not crash when the API or the internet has a problem.
- It was hard to choose a level. Level A has more work and more rules.

## Solutions

- I read the level A rules again. The basic parts (model client, tools, tests) are the same as level C, so my work so far is not lost. I will add the A parts step by step in weeks 12 to 15.
- I used `try/except` to catch errors, and I made one special error type (`LLMError`) with a clear message. I tested these cases with a fake API.

## What I Learned

- How to handle errors and how to test code with a fake API (mock).
- AI help: I used an AI assistant (Claude) to write the first version of the code.

## Next Week

- Think about the research paper for level A.
- Create the fake course data (courses, credits, exam dates, deadlines).
- Write the functions `get_course_info`, `get_student_courses` and `get_course_deadlines`.
- Check inputs and outputs, and ask the LLM for structured (JSON) answers.
- Write the first tests for these functions.
