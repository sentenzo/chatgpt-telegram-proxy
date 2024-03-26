import asyncio

from openai_connect.ai.impl import UglyOpenAi
from openai_connect.bot import Bot
from openai_connect.messenger.impl import CliMessenger
from openai_connect.queue.impl import AsyncIoQueue

asyncio.run(
    Bot(CliMessenger(), AsyncIoQueue(), AsyncIoQueue(), UglyOpenAi()).launch()
)
