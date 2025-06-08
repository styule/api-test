import os
import openai
import json
from dotenv import load_dotenv
from agentcore import Agent

from .tools import (
    get_time,
    reverse_text,
    calculator,
    get_weather,
    summarize_file,
    define_word,
)

functions = [
    {
        "name": "get_time",
        "description": "Get the current system time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "reverse_text",
        "description": "Reverse a string.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The text to reverse."},
            },
            "required": ["text"],
        },
    },
    {
        "name": "calculator",
        "description": (
            "Evaluate a mathematical expression (e.g., '2 + 2 * 3'). "
            "Only pass the expression, with no extra words or punctuation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate.",
                },
            },
            "required": ["expression"],
        },
    },
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name."},
            },
            "required": ["city"],
        },
    },
    {
        "name": "summarize_file",
        "description": "Read and return the contents of a .txt file for summarization.",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {
                    "type": "string",
                    "description": "Full path to a .txt file.",
                },
            },
            "required": ["filepath"],
        },
    },
    {
        "name": "define_word",
        "description": "Look up the definition of an English word.",
        "parameters": {
            "type": "object",
            "properties": {
                "word": {"type": "string", "description": "The word to define."},
            },
            "required": ["word"],
        },
    },
]


load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def main():
    print("Type your prompt ('exit' to quit):")
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that can use tools. "
                "When calling calculator function, pass only mathematical expression "
                "(e.g., '2 + 2 * 3'), with no extra text, words, or punctuation."
            ),
        }
    ]

    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            functions=functions,
            function_call="auto",
        )
        msg = response.choices[0].message

        if msg.function_call:
            fn_name = msg.function_call.name
            args = json.loads(msg.function_call.arguments)
            if fn_name == "get_time":
                result = get_time()
            elif fn_name == "reverse_text":
                result = reverse_text(**args)
            elif fn_name == "calculator":
                result = calculator(**args)
            elif fn_name == "get_weather":
                result = get_weather(**args)
            elif fn_name == "summarize_file":
                result = summarize_file(**args)
            elif fn_name == "define_word":
                result = define_word(**args)
            else:
                result = {"error": f"Unknown function: {fn_name}"}

            messages.append(msg.model_dump())
            messages.append(
                {
                    "role": "function",
                    "name": fn_name,
                    "content": json.dumps(result),
                }
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                functions=functions,
            )
            print(response.choices[0].message.content)
            messages.append(response.choices[0].message.model_dump())
        else:
            print(msg.content)
            messages.append(msg.model_dump())


if __name__ == "__main__":
    main()


__all__ = ["Agent"]
