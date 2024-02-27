import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN", default="")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    await message.answer("Hello from `aiogram` lib!")


def main() -> None:
    asyncio.run(dp.start_polling(bot))


if __name__ == "__main__":
    main()
