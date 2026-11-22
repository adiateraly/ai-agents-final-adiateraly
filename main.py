"""Academic Planner Agent - command line.

Commands:
    python main.py "your question"      ask the LLM (same as: ask)
    python main.py ask "your question"  ask the LLM
    python main.py course AI101         LLM summary of a course (checked JSON)
    python main.py data S001            show the fake data (no LLM, no key)
    python main.py data AI101
"""

import json
import sys

from src import tools
from src.model_client import LLMError, complete, load_env
from src.structured import StructuredOutputError, summarize_course
from src.validation import check_course_id, check_student_id

SYSTEM_PROMPT = (
    "You are a helpful assistant for university students. "
    "Answer in simple English and keep answers short."
)


def ask(question):
    """Send one question to the LLM and return the text answer."""
    question = (question or "").strip()
    if not question:
        raise ValueError("Please write a question.")
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    return complete(messages)["text"]


def show_data(identifier):
    """Print fake data for a student ID or a course ID (no LLM needed)."""
    if check_student_id(identifier) is None:
        courses = tools.get_student_courses(identifier)
        print(json.dumps(courses, indent=2))
        if isinstance(courses, list):
            for course_id in courses:
                show_data(course_id)
    elif check_course_id(identifier) is None:
        print(identifier, json.dumps(tools.get_course_info(identifier)))
        print(identifier, json.dumps(tools.get_course_deadlines(identifier)))
    else:
        raise ValueError("Use an ID like S001 or AI101.")


def main():
    load_env()
    args = sys.argv[1:]
    if not args:
        args = ["ask", input("Your question: ")]
    command = args[0]
    try:
        if command == "course" and len(args) == 2:
            print(json.dumps(summarize_course(args[1]), indent=2))
        elif command == "data" and len(args) == 2:
            show_data(args[1])
        elif command == "ask":
            print(ask(" ".join(args[1:])))
        else:
            print(ask(" ".join(args)))
    except ValueError as error:
        print("Input error:", error)
        sys.exit(1)
    except (LLMError, StructuredOutputError) as error:
        print("Error:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
