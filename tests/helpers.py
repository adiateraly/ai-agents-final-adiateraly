"""Helpers for tests: a fake LLM that returns prepared answers."""

import copy


class ScriptedLLM:
    """A fake model. Give it a list of answers; it returns them one by one."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def __call__(self, messages, tools=None):
        self.calls.append({"messages": copy.deepcopy(messages), "tools": tools})
        if not self.responses:
            raise AssertionError("The fake model has no more answers.")
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def text_response(text):
    """A model answer that is only text."""
    return {"text": text, "tool_calls": [], "message": {"role": "assistant", "content": text}}
