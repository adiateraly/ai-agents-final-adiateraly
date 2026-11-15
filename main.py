"""First working request to the LLM.

Run:
    python main.py "Say hello in one short sentence."
or run without text and type your question when the program asks.
"""

import sys

from src.model_client import LLMError, complete, load_env

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


def main():
    load_env()
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = input("Your question: ")
    try:
        print(ask(question))
    except ValueError as error:
        print("Input error:", error)
        sys.exit(1)
    except LLMError as error:
        print("LLM error:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
