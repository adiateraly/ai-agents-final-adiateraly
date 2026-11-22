import unittest

from src.validation import is_valid_date, validate_tool_args, validate_tool_output


class ValidationTests(unittest.TestCase):
    def test_valid_arguments_are_accepted(self):
        self.assertTrue(validate_tool_args("get_course_info", {"course_id": "AI101"})["ok"])
        self.assertTrue(validate_tool_args("get_student_courses", {"student_id": "S001"})["ok"])

    def test_wrong_type_is_rejected(self):
        self.assertFalse(validate_tool_args("get_course_info", {"course_id": 101})["ok"])

    def test_wrong_format_is_rejected(self):
        self.assertFalse(validate_tool_args("get_course_info", {"course_id": "ai 101; drop"})["ok"])
        self.assertFalse(validate_tool_args("get_student_courses", {"student_id": "S001\n"})["ok"])

    def test_missing_and_extra_arguments_are_rejected(self):
        self.assertFalse(validate_tool_args("get_course_info", {})["ok"])
        self.assertFalse(validate_tool_args("get_course_info", {"course_id": "AI101", "x": 1})["ok"])

    def test_unknown_tool_is_rejected(self):
        self.assertFalse(validate_tool_args("delete_files", {})["ok"])

    def test_dates(self):
        self.assertTrue(is_valid_date("2026-12-15"))
        self.assertFalse(is_valid_date("2026-13-40"))
        self.assertFalse(is_valid_date("15-12-2026"))

    def test_bad_tool_output_is_rejected(self):
        self.assertFalse(validate_tool_output("get_course_info", {"title": "X", "credits": -1, "exam_date": "2026-12-15"})["ok"])
        self.assertFalse(validate_tool_output("get_course_deadlines", [{"date": "bad", "title": "X"}])["ok"])
        self.assertTrue(validate_tool_output("get_course_info", {"error": "Course not found"})["ok"])


if __name__ == "__main__":
    unittest.main()
