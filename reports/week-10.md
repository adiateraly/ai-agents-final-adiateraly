# Semester Week 10 Progress Report

## Completed Work

- I forked the instructor's repository to my own GitHub account.
- I read the README, the level C and level A requirements, the grading rules and the weekly plan.
- I chose my project topic: Academic Planner Agent. It answers questions about courses and deadlines with tools. Later it can make a study plan.
- I chose level C. I plan to move to level A if the work goes well. The same three tools can be used in both levels.
- I wrote the full project proposal in `reports/proposal.md`. It has the problem, users, functions, tools, model, architecture, example requests, test plan and weekly milestones.

## Important Commits

- Commit hash: I will add it after my first push to GitHub.
- Description: finished `reports/proposal.md` and `reports/week-10.md`.
- Link: I will add the link to this commit in my fork.

## Current Functionality

The application code does not exist yet. This week was only for planning. The repository now has a proposal with the planned functions, tools, architecture and tests. The checks `npm run proposal` and `npm run report -- 10` pass for these files.

## Problems Encountered

- It was difficult to choose between level C and level A before I started to write code.

## Solutions

- I compared the requirements. Level A has everything from level C and some extra parts. So I chose level C as a safe start. I made a plan where level A parts can be added later.
- I chose a topic that I know well (university courses) and simple fake data. This helps me focus on learning how an agent works.
- I will decide about level A in week 14. I will write the decision in my report.

## What I Learned

- An LLM agent is a program where the AI model chooses a tool, the program runs the tool, and the AI uses the result to answer.
- Level D is an AI application with checked output. Level C adds tools chosen by the AI. Level A adds many steps, state, limits and safety rules.
- An API key must stay in a `.env` file. I must never upload it to GitHub.
- Weekly work is important. The final score is multiplied by a coefficient that depends on the number of active weeks.
- AI help: I used an AI assistant (Claude) to understand the task.

## Next Week

- Make a `.env` file from `.env.example` and get an API key.
- Write `src/model_client.py` (Python) to send a request to the AI model and read the answer.
- Make the first working request and show the answer in the terminal.
- Write a short README with setup and run steps.
- Commit and push the working prototype to GitHub.
