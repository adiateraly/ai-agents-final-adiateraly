import unittest

from src import tools
from src.validation import validate_tool_output


class ToolTests(unittest.TestCase):
    def test_student_courses(self):
        self.assertEqual(tools.get_student_courses("S001"), ["AI101", "ML201"])

    def test_unknown_student(self):
        self.assertEqual(tools.get_student_courses("S999"), {"error": "Student not found"})

    def test_course_info(self):
        info = tools.get_course_info("AI101")
        self.assertEqual(info["exam_date"], "2026-12-15")
        self.assertEqual(info["credits"], 5)

    def test_unknown_course(self):
        self.assertEqual(tools.get_course_info("CS999"), {"error": "Course not found"})
        self.assertEqual(tools.get_course_deadlines("CS999"), {"error": "Course not found"})

    def test_deadlines_and_changing_the_result_does_not_change_the_data(self):
        deadlines = tools.get_course_deadlines("ML201")
        deadlines.append({"date": "2030-01-01", "title": "Fake"})
        self.assertEqual(len(tools.get_course_deadlines("ML201")), 2)

    def test_all_real_results_pass_output_validation(self):
        for name, arg in [("get_student_courses", "S001"), ("get_course_info", "AI101"),
                          ("get_course_deadlines", "DB101"), ("get_course_notes", "ML201")]:
            result = getattr(tools, name)(arg)
            self.assertTrue(validate_tool_output(name, result)["ok"], name)


if __name__ == "__main__":
    unittest.main()
