import os
from datetime import datetime
from typing import AsyncGenerator

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from openai_connect.ai import Ai
from openai_connect.message import Message, MessageType

API_KEY = os.environ.get("OPENAI_API_KEY", default="")
BASE_URL = os.environ.get("OPENAI_API_BASE_URL", default="")
DEFAULT_MODEL = os.environ.get("OPENAI_API_DEFAULT_MODEL", default="")

INIT_PROMPT: list[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": (
            "You are an intelligent assistant. You always provide "
            "well-reasoned answers that are both correct and helpful."
        ),
    },
    {
        "role": "user",
        "content": (
            "Hello, introduce yourself to someone opening "
            "this program for the first time. Be concise."
        ),
    },
]


class UglyOpenAi(Ai):
    def __init__(self) -> None:
        self.client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
        self.history: dict[str, list[ChatCompletionMessageParam]] = {}

    async def reply(
        self, message: Message, stream: bool = False
    ) -> AsyncGenerator[Message, None]:
        key = message.chat_id
        if key not in self.history:
            self.history[key] = INIT_PROMPT[:]
        else:
            self.history[key].append(
                {"role": "user", "content": message.message_text or ""}
            )

        completion = await self.client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=self.history[key],
            temperature=0.7,
            max_tokens=1000,
        )
        text = completion.choices[0].message.content or ""
        self.history[key].append({"role": "assistant", "content": text})
        yield Message(
            int(datetime.now().timestamp()),
            MessageType.OUTGOING,
            chat_id=message.chat_id,
            user_id=f"assistant-{message.chat_id}",
            message_id=None,
            message_text=text,
        )
