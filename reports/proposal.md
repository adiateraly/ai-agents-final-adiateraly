# Project Proposal — Semester Week 10

## Project Title

Academic Planner Agent — a smart helper for university courses and deadlines.

## Problem Description

Students have course information in many places: credits, exam dates and homework deadlines. To find one answer, a student must open many pages and compare dates by hand. This takes time. Sometimes students miss a deadline.

My application solves this problem. The student asks a question in simple words. The AI model (LLM) chooses which tool to use. The program gets real data with this tool. Then the AI gives an answer based on this data. The AI does not guess.

This is important because it saves time. It also shows how to use an AI model safely with real data.

## Target Users

University students who want fast answers about their courses, exam dates and deadlines. Later, they can also get a simple study plan. The project uses fake (mock) data, so there is no real personal data.

## Selected Difficulty

C — Intermediate (an agent that uses tools).

Plan for later: move to level A if the work goes well. Level A adds more steps, memory of the task (state), limits, safety rules (guardrails) and a research paper presentation. I chose a topic where level A can be added on top of level C. I will write any change of level in my weekly reports.

## Expected Functionality

- Answer questions about a course (title, credits, exam date) with a tool.
- Answer questions about a student's courses and deadlines with tools.
- The AI model chooses the tool and the tool arguments by itself.
- Answer simple questions without a tool (for example, "Hello").
- Say clearly when data does not exist (for example, course CS999). Do not invent an answer.
- Check all tool arguments and all AI outputs before use.
- Handle errors from the API and from the tools. The program must not crash.
- Save a log of every tool call (tool name, arguments, result or error).
- Possible level A features: a task with many steps, such as "Find all deadlines for student S001 and make a study plan"; saving the plan only after the user says yes; limits on steps; a full trace of the work.

## Proposed Functions

All functions are in Python. The data is in a local file with fake data.

1. `get_student_courses(student_id)`
   - Purpose: give the course IDs of a student.
   - Input: `student_id`, a text like "S001".
   - Output: a list like `["AI101", "ML201"]`, or an error if the student does not exist.
   - Dependencies: mock data.
2. `get_course_info(course_id)`
   - Purpose: give the title, credits and exam date of a course.
   - Input: `course_id`, a text like "AI101".
   - Output: a dictionary with title, credits and exam date, or `{"error": "Course not found"}`.
   - Dependencies: mock data.
3. `get_course_deadlines(course_id)`
   - Purpose: give the deadlines of a course.
   - Input: `course_id`.
   - Output: a list of dates like "2026-12-10", or an error if the course does not exist.
   - Dependencies: mock data.
4. `validate_tool_args(tool_name, args)`
   - Purpose: reject wrong arguments before the tool runs.
   - Input: tool name and arguments from the AI model.
   - Output: `{"ok": True}` or `{"ok": False, "error": ...}`.
   - Dependencies: tool descriptions.
5. `complete(messages, tools)`
   - Purpose: send a request to the AI model API and get the answer.
   - Input: messages and a list of tools.
   - Output: text and tool calls requested by the model.
   - Dependencies: API key and model name from the `.env` file.
6. `run_agent(user_request)`
   - Purpose: the main loop. Send the request to the AI, run the tools it asks for, send the results back, and repeat until the final answer.
   - Input: the user's text.
   - Output: the final answer and a log of tool calls.
   - Dependencies: functions 1 to 5.
7. `log_tool_call(entry)`
   - Purpose: save each tool call in a log. No secret data in the log.
   - Input: tool name, arguments, result or error.
   - Output: one line in the log.
   - Dependencies: none.
8. `save_study_plan(path, content)` (planned for level A)
   - Purpose: save the study plan to a file. This action needs the user's approval.
   - Input: a file name in an allowed folder, and the plan text.
   - Output: success or error, after checking that the file exists.
   - Dependencies: file system, approval step.

## Proposed Agent Tools

These functions are tools that the AI model can call:

- `get_student_courses` (function 1). The agent needs it to know the student's courses before it asks about deadlines.
- `get_course_info` (function 2). The agent needs it to answer about credits, title and exam date with real data.
- `get_course_deadlines` (function 3). The agent needs it to get real deadlines. Without it the AI would guess dates.

These are three tools. Level C needs two tools and level A needs three, so this is enough for both. The planned tool `save_study_plan` (function 8) can work only after the user approves.

Functions 4, 6 and 7 are inside the program. The AI model cannot call them. The three data tools can only read data. The program (not only the prompt) blocks any tool that is not on the allowed list.

## Model Selection

I will use the OpenAI API with tool calling (function calling). The API key and model name are saved in a local `.env` file. This file is not uploaded to GitHub. The program uses only the standard Python library (`urllib`), so it needs no extra packages. In tests I will use a fake model, so tests are fast, always give the same result, and need no API key.

## Architecture

Basic workflow (level C):

```text
User request
    ↓
run_agent ──► AI model (model_client.py)
               │
               ├── no tool needed ───────────► Final answer
               │
               └── tool call requested
                      ↓
                validate_tool_args ── wrong ──► error goes back to the AI
                      ↓ correct
                run the tool (mock data)
                      ↓
                log_tool_call
                      ↓
                result goes back to the AI ──► Final answer
```

Possible level A additions: task state, a limit of steps and tool calls, stop rules, retry after an error, user approval before saving a file, and a full trace.

## Example Requests

1. "When is the AI101 exam?" The agent calls `get_course_info("AI101")` and answers "2026-12-15".
2. "How many credits does ML201 have?" The agent calls `get_course_info("ML201")` and answers "6".
3. "What is the exam date for CS999?" The tool says "Course not found". The agent says this course does not exist. It does not invent a date.
4. "Hello, what can you do?" The agent answers without a tool.
5. (Level A) "Find all deadlines for student S001 and make a study plan." The agent gets the courses, then the deadlines of each course, puts the dates in order and writes a plan.

## Evaluation Plan

I will check the system with automatic tests (`python -m unittest`). The tests use a fake AI model and fake data. I will also try the real model by hand.

Planned tests for level C (at least 8):

1. A course question makes the agent call `get_course_info` with the right argument.
2. The final answer has the real value from the tool.
3. An unknown course gives an error, and the answer has no invented data.
4. A simple question gets an answer without a tool call.
5. Wrong tool arguments are rejected before the tool runs.
6. A tool error is handled and the program does not crash.
7. An API error is handled with a clear message.
8. Every tool call is saved in the log with name, arguments and result.

If I move to level A, I will have at least 12 tests. Four tests will check safety: a prompt injection in a document, a tool that fails again and again, an action without approval, and the step limit.

The project is successful when all tests pass, answers match the data, and the agent never gives a value that a tool did not return.

## Weekly Milestones

- Week 10 (2–8 Nov): fork the repository, choose topic and level, write the proposal and the week-10 report.
- Week 11 (9–15 Nov): prepare the environment and the `.env` file, write the model client, make the first working request, write a short README.
- Week 12 (16–22 Nov): add fake data and three functions, check inputs and outputs, write the first tests.
- Week 13 (23–29 Nov): give the tools to the AI model, let it choose tools, run real tool calls, check tool arguments.
- Week 14 (30 Nov–6 Dec): finish the tool workflow, handle tool errors, add logs. Decide: stay at level C or move to level A (state, many steps, stop rules). For level A, choose the research paper.
- Week 15 (7–13 Dec): make the program more reliable. For level A, add safety rules, limits, approval, trace and safety tests.
- Week 16 (14–20 Dec): run all tests, save the results, find and fix problems, update the documents. For level A, prepare the paper presentation.
- Week 17 (21–22 Dec): final README, final commit hash, demonstration and defense.
