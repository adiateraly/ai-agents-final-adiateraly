"""Structured output: ask the LLM for JSON and check it before we use it."""

import json

from src.model_client import complete
from src.tools import get_course_deadlines, get_course_info
from src.validation import validate_tool_args


class StructuredOutputError(Exception):
    """Raised when the model answer is not the JSON we asked for."""


def extract_json(text):
    """Find the JSON object in a model answer (it may have ``` fences around it)."""
    if not isinstance(text, str) or not text.strip():
        raise StructuredOutputError("The answer is empty.")
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise StructuredOutputError("The answer has no JSON object.")
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        raise StructuredOutputError("The answer is not valid JSON.")


def validate_summary(data, course_id):
    """Check the course summary. Raises StructuredOutputError if something is wrong."""
    if not isinstance(data, dict):
        raise StructuredOutputError("The JSON must be an object.")
    if data.get("course_id") != course_id:
        raise StructuredOutputError("course_id is missing or wrong.")
    summary = data.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        raise StructuredOutputError("summary must be a non-empty text.")
    tips = data.get("tips")
    if not isinstance(tips, list) or not 2 <= len(tips) <= 5:
        raise StructuredOutputError("tips must be a list of 2 to 5 items.")
    if any(not isinstance(tip, str) or not tip.strip() for tip in tips):
        raise StructuredOutputError("each tip must be a non-empty text.")
    return data


def summarize_course(course_id, llm=complete, max_attempts=2):
    """Ask the LLM for a short study summary of a course, as checked JSON."""
    check = validate_tool_args("get_course_info", {"course_id": course_id})
    if not check["ok"]:
        raise ValueError(check["error"])
    info = get_course_info(course_id)
    if "error" in info:
        raise ValueError(info["error"])
    course_data = {"course_id": course_id, "info": info, "deadlines": get_course_deadlines(course_id)}

    messages = [
        {"role": "system", "content": "You help university students. Reply with JSON only. Use simple English."},
        {
            "role": "user",
            "content": (
                "Write a short study summary for this course.\n"
                'Reply with JSON only, in this format: {"course_id": "<id>", "summary": "<1-2 simple sentences>", '
                '"tips": ["<tip 1>", "<tip 2>"]}\n'
                "Use only this data:\n" + json.dumps(course_data)
            ),
        },
    ]
    last_error = "No answer."
    for _ in range(max_attempts):
        text = llm(messages)["text"]
        try:
            return validate_summary(extract_json(text), course_id)
        except StructuredOutputError as error:
            last_error = str(error)
            messages.append({"role": "assistant", "content": text})
            messages.append({"role": "user", "content": "That was not valid: {} Reply again with JSON only.".format(last_error)})
    raise StructuredOutputError("The model did not give valid JSON. " + last_error)
