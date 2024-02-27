import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN", default="")


bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=["start"])
async def send_welcome(message: Message) -> None:
    await bot.reply_to(message, "Hello from `telebot` lib!")


@bot.message_handler(func=lambda message: True)
async def echo_message(message: Message) -> None:
    await bot.reply_to(message, message.text)


def main() -> None:
    asyncio.run(bot.polling())
