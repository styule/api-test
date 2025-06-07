#!/usr/bin/env python3
"""
example.py
A CLI tool that sends a prompt to OpenAI, prints the assistant’s reply,
and appends the exchange to conversation_log.jsonl.
"""

import os
import sys
import argparse
import logging
import json
from datetime import datetime

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError


# 1. Load .env (if present) and read key
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    sys.exit("❌ ERROR: Set OPENAI_API_KEY in your environment or .env")


# 2. Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)


# 3. Instantiate client
client = OpenAI(api_key=API_KEY)


def ask_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """
    Send prompt to the chosen model and return the assistant’s reply.
    """
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user",   "content": prompt}
            ],
        )
        return resp.choices[0].message.content or ""
    except OpenAIError as e:
        logging.error(f"OpenAI API error: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Send a prompt to OpenAI and print the response."
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help=(
            "The text to send to the model; "
            "if omitted, you will be prompted interactively"
        ),
    )
    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="Model name (e.g. gpt-4, gpt-3.5-turbo).",
    )
    args = parser.parse_args()

    if args.prompt is None:
        args.prompt = input("Enter your prompt: ")

    logging.info(f"Sending prompt to {args.model}")
    reply = ask_openai(args.prompt, model=args.model)

    print("\n🗨️  Assistant says:\n")
    print(reply)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "model":     args.model,
        "prompt":    args.prompt,
        "response":  reply,
    }
    with open("conversation_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False))
        f.write("\n")


if __name__ == "__main__":
    main()
