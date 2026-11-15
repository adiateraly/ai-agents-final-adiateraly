"""Tests for src/model_client.py. They use a fake API, so no key or internet is needed."""

import io
import json
import os
import unittest
import urllib.error
from unittest import mock

from src import model_client
from src.model_client import LLMError, complete

FAKE_ENV = {"LLM_API_KEY": "test-key", "LLM_MODEL": "test-model"}


def api_answer(content="Hello!", tool_calls=None):
    message = {"role": "assistant", "content": content}
    if tool_calls:
        message["tool_calls"] = tool_calls
    return {"choices": [{"message": message}]}


class ModelClientTests(unittest.TestCase):
    def setUp(self):
        # Do not wait between retries in tests.
        patcher = mock.patch.object(model_client, "RETRY_WAIT_SECONDS", 0)
        patcher.start()
        self.addCleanup(patcher.stop)

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_returns_text_from_model(self):
        with mock.patch.object(model_client, "_post_json", return_value=api_answer("Hi there")):
            result = complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(result["text"], "Hi there")
        self.assertEqual(result["tool_calls"], [])

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_parses_tool_call_arguments(self):
        call = {"id": "c1", "function": {"name": "get_course_info", "arguments": '{"course_id": "AI101"}'}}
        with mock.patch.object(model_client, "_post_json", return_value=api_answer(None, [call])):
            result = complete([{"role": "user", "content": "When is AI101?"}])
        self.assertEqual(result["tool_calls"][0]["name"], "get_course_info")
        self.assertEqual(result["tool_calls"][0]["arguments"], {"course_id": "AI101"})

    @mock.patch.dict(os.environ, {"LLM_MODEL": "test-model"}, clear=True)
    def test_missing_api_key_gives_clear_error(self):
        with self.assertRaises(LLMError) as context:
            complete([{"role": "user", "content": "Hello"}])
        self.assertIn("LLM_API_KEY", str(context.exception))

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_empty_messages_are_rejected(self):
        with self.assertRaises(LLMError):
            complete([])

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_wrong_key_is_not_retried_and_key_is_not_shown(self):
        error = urllib.error.HTTPError("url", 401, "Unauthorized", {}, io.BytesIO(b"{}"))
        with mock.patch.object(model_client, "_post_json", side_effect=error) as post:
            with self.assertRaises(LLMError) as context:
                complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(post.call_count, 1)
        self.assertIn("401", str(context.exception))
        self.assertNotIn("test-key", str(context.exception))

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_network_error_is_retried_then_reported(self):
        error = urllib.error.URLError("no internet")
        with mock.patch.object(model_client, "_post_json", side_effect=error) as post:
            with self.assertRaises(LLMError) as context:
                complete([{"role": "user", "content": "Hello"}])
        self.assertEqual(post.call_count, model_client.MAX_RETRIES + 1)
        self.assertIn("Network problem", str(context.exception))

    @mock.patch.dict(os.environ, FAKE_ENV, clear=True)
    def test_unexpected_api_format_is_reported(self):
        with mock.patch.object(model_client, "_post_json", return_value={"oops": 1}):
            with self.assertRaises(LLMError):
                complete([{"role": "user", "content": "Hello"}])

    def test_load_env_reads_file_and_keeps_existing_values(self):
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, ".env")
            with open(path, "w", encoding="utf-8") as file:
                file.write('# comment\nLLM_API_KEY="from-file"\nLLM_MODEL=model-from-file\n')
            with mock.patch.dict(os.environ, {"LLM_MODEL": "already-set"}, clear=True):
                model_client.load_env(path)
                self.assertEqual(os.environ["LLM_API_KEY"], "from-file")
                self.assertEqual(os.environ["LLM_MODEL"], "already-set")


if __name__ == "__main__":
    unittest.main()
