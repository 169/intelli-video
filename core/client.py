from typing import Generator
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def translate(prompt) -> Generator:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=OPENAI_MODEL,
    )
    for text in chat_completion.choices[0].message.content.split("\n"):
        if text:
            yield text
