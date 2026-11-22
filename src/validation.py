"""Checks for tool arguments (before a tool runs) and tool results (after).

Every check returns None when the value is fine, or a short error text.
"""

import re
from datetime import datetime

STUDENT_ID_PATTERN = re.compile(r"S\d{3}")
COURSE_ID_PATTERN = re.compile(r"[A-Z]{2,4}\d{3}")


def is_valid_date(text):
    """True if text is a real date in the format YYYY-MM-DD."""
    if not isinstance(text, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        return False
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def check_student_id(value):
    if not isinstance(value, str):
        return "student_id must be a text"
    if not STUDENT_ID_PATTERN.fullmatch(value):
        return "student_id must look like S001"
    return None


def check_course_id(value):
    if not isinstance(value, str):
        return "course_id must be a text"
    if not COURSE_ID_PATTERN.fullmatch(value):
        return "course_id must look like AI101"
    return None


# For every tool: which arguments it needs and how to check each one.
ARGUMENT_RULES = {
    "get_student_courses": {"student_id": check_student_id},
    "get_course_info": {"course_id": check_course_id},
    "get_course_deadlines": {"course_id": check_course_id},
    "get_course_notes": {"course_id": check_course_id},
}


def validate_tool_args(tool_name, args):
    """Check the arguments of a tool call. Returns {"ok": True} or {"ok": False, "error": ...}."""
    if tool_name not in ARGUMENT_RULES:
        return {"ok": False, "error": "Unknown tool: {}".format(tool_name)}
    if not isinstance(args, dict):
        return {"ok": False, "error": "Arguments must be a JSON object"}
    rules = ARGUMENT_RULES[tool_name]
    for name in rules:
        if name not in args:
            return {"ok": False, "error": "Missing argument: {}".format(name)}
    for name in args:
        if name not in rules:
            return {"ok": False, "error": "Unexpected argument: {}".format(name)}
    for name, check in rules.items():
        problem = check(args[name])
        if problem:
            return {"ok": False, "error": problem}
    return {"ok": True}


def _is_error_result(result):
    return isinstance(result, dict) and "error" in result


def validate_tool_output(tool_name, result):
    """Check the result of a tool. An error result from a tool is allowed."""
    if _is_error_result(result):
        return {"ok": True}
    problem = None
    if tool_name == "get_student_courses":
        if not isinstance(result, list) or any(check_course_id(c) for c in result):
            problem = "courses must be a list of course IDs"
    elif tool_name == "get_course_info":
        if not isinstance(result, dict):
            problem = "course info must be a dictionary"
        elif not isinstance(result.get("title"), str) or not result["title"].strip():
            problem = "course info needs a title"
        elif not isinstance(result.get("credits"), int) or result["credits"] <= 0:
            problem = "course info needs positive credits"
        elif not is_valid_date(result.get("exam_date")):
            problem = "course info needs a valid exam_date"
    elif tool_name == "get_course_deadlines":
        if not isinstance(result, list):
            problem = "deadlines must be a list"
        else:
            for item in result:
                if not isinstance(item, dict) or not is_valid_date(item.get("date")) \
                        or not isinstance(item.get("title"), str) or not item["title"].strip():
                    problem = "each deadline needs a valid date and a title"
                    break
    elif tool_name == "get_course_notes":
        if not isinstance(result, str):
            problem = "notes must be a text"
    else:
        problem = "Unknown tool: {}".format(tool_name)
    if problem:
        return {"ok": False, "error": problem}
    return {"ok": True}
