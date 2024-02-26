from .aiogram.bot import main as agr_main
from .python_telegram_bot.bot import main as ptb_main
from .telebot.bot import main as tbt_main

__all__ = ["ptb_main", "agr_main", "tbt_main"]
