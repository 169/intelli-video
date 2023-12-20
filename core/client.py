import json
from typing import Literal

from loguru import logger
from openai import OpenAI
from tenacity import retry, stop_after_attempt

from config import DEBUG, OPENAI_API_KEY, OPENAI_MODEL


class Client:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def translate(self, prompt) -> dict:
        if DEBUG:
            logger.debug(prompt)
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=OPENAI_MODEL,
            response_format={"type": "json_object"},
        )

        return json.loads(chat_completion.choices[0].message.content)

    @retry(stop=stop_after_attempt(3))
    def transcribe(
        self,
        audio: str,
        response_format: Literal["vvt", "srt"] = "vtt",
        language="en",
    ) -> str:
        transcript = self.client.audio.transcriptions.create(
            model="whisper-1",
            language=language,
            file=open(audio, "rb"),
            response_format=response_format,
        )
        return transcript
