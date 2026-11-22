"""The data tools. They only READ the fake data in src/data.py.

On success a tool returns the data. On failure it returns {"error": "..."}.
"""

import copy

from src import data


def get_student_courses(student_id):
    """Return the list of course IDs of a student."""
    courses = data.STUDENTS.get(student_id)
    if courses is None:
        return {"error": "Student not found"}
    return list(courses)


def get_course_info(course_id):
    """Return title, credits and exam date of a course."""
    info = data.COURSES.get(course_id)
    if info is None:
        return {"error": "Course not found"}
    return copy.deepcopy(info)


def get_course_deadlines(course_id):
    """Return the list of deadlines (date and title) of a course."""
    deadlines = data.DEADLINES.get(course_id)
    if deadlines is None:
        return {"error": "Course not found"}
    return copy.deepcopy(deadlines)


def get_course_notes(course_id):
    """Return the teacher's notes of a course (untrusted text)."""
    note = data.NOTES.get(course_id)
    if note is None:
        return {"error": "Course not found"}
    return note
