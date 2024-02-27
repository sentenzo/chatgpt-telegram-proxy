import os
from pathlib import Path

from telethon import TelegramClient, events
from telethon.tl.custom.message import Message

TOKEN = os.environ.get("TELEGRAM_BOT_API_TOKEN", default="")
API_ID = int(os.environ.get("TELEGRAM_APP_API_ID", default="0"))
API_HASH = os.environ.get("TELEGRAM_APP_API_HASH", default="")

SESSION_DIR = Path(".telethon_sessions")
SESSION_DIR.mkdir(exist_ok=True)

session_name = str(SESSION_DIR / "bot")

bot = TelegramClient(session_name, API_ID, API_HASH)
bot.start(bot_token=TOKEN)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event: Message) -> None:
    await event.respond("Hello from `telethon` lib!")
    raise events.StopPropagation


@bot.on(events.NewMessage)
async def echo(event: Message) -> None:
    await event.respond(event.text)


def main() -> None:
    bot.run_until_disconnected()
