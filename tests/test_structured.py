import json
import unittest

from src.structured import StructuredOutputError, extract_json, summarize_course
from tests.helpers import ScriptedLLM, text_response

GOOD = {"course_id": "AI101", "summary": "A course about AI.", "tips": ["Start early.", "Practice."]}


class StructuredTests(unittest.TestCase):
    def test_valid_json_is_returned(self):
        llm = ScriptedLLM([text_response(json.dumps(GOOD))])
        self.assertEqual(summarize_course("AI101", llm=llm), GOOD)

    def test_json_inside_code_fences_is_read(self):
        self.assertEqual(extract_json("```json\n" + json.dumps(GOOD) + "\n```"), GOOD)

    def test_invalid_answer_is_retried_once(self):
        llm = ScriptedLLM([text_response("Sorry, I cannot."), text_response(json.dumps(GOOD))])
        self.assertEqual(summarize_course("AI101", llm=llm), GOOD)
        self.assertEqual(len(llm.calls), 2)

    def test_always_invalid_raises_clear_error(self):
        bad = {"course_id": "AI101", "summary": "", "tips": ["one"]}
        llm = ScriptedLLM([text_response(json.dumps(bad)), text_response(json.dumps(bad))])
        with self.assertRaises(StructuredOutputError):
            summarize_course("AI101", llm=llm)

    def test_bad_or_unknown_course_is_rejected_before_calling_the_llm(self):
        llm = ScriptedLLM([])
        with self.assertRaises(ValueError):
            summarize_course("not a course", llm=llm)
        with self.assertRaises(ValueError):
            summarize_course("CS999", llm=llm)
        self.assertEqual(llm.calls, [])


if __name__ == "__main__":
    unittest.main()
