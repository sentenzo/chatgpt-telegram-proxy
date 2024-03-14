import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters.command import CommandStart
from aiogram.types import Message
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN", default="")

API_KEY = os.environ.get("OPENAI_API_KEY", default="")
BASE_URL = os.environ.get("OPENAI_API_BASE_URL", default="")
DEFAULT_MODEL = os.environ.get("OPENAI_API_DEFAULT_MODEL", default="")

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

SYS_PROMPT: list[ChatCompletionMessageParam] = [
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

HISTORY: dict[str, list[ChatCompletionMessageParam]] = {}


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    key = str(message.chat.id)
    HISTORY[key] = SYS_PROMPT[:]
    await message.chat.do("typing")
    completion = await client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=HISTORY[key],
        temperature=0.7,
        max_tokens=1000,
    )
    text = completion.choices[0].message.content or ""
    HISTORY[key].append({"role": "assistant", "content": text})
    await message.answer(text)


@dp.message()
async def cmd_default_responce(message: Message) -> None:
    key = str(message.chat.id)
    HISTORY[key].append({"role": "user", "content": message.text or ""})
    await message.chat.do("typing")
    completion = await client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=HISTORY[key],
        temperature=0.7,
        max_tokens=1000,
    )
    text = completion.choices[0].message.content or ""
    HISTORY[key].append({"role": "assistant", "content": text})
    await message.answer(text)


def main() -> None:
    asyncio.run(dp.start_polling(bot))
