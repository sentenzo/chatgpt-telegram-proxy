import os
from collections import deque

from aiogram import Bot, Dispatcher
from aiogram.types import Message as MessageData
from telegram.constants import UpdateType

from openai_connect.message import Message, MessageType
from openai_connect.messenger import Messenger

INBOX_SIZE = 50


class AiogramMessenger(Messenger):
    def __init__(self, token: str | None = None) -> None:
        token = token or os.environ.get("TELEGRAM_BOT_API_TOKEN") or ""
        self.telegram_bot = Bot(token=token)
        self.dispatcher = Dispatcher()
        self.inbox: deque[MessageData] = deque()

    @staticmethod
    def create_incoming_message(message_data: MessageData) -> Message:
        created_at = int(message_data.date.timestamp())
        chat_id = str(message_data.chat.id)
        user = message_data.from_user
        user_id = None if user is None else str(user.id)
        message_id = str(message_data.message_id)
        message_text = message_data.text
        return Message(
            created_at,
            MessageType.INCOMING,
            chat_id,
            user_id,
            message_id,
            message_text,
        )

    async def receive_message(self) -> Message:
        if not self.inbox:
            new_updates = await self.telegram_bot.get_updates(
                offset=-INBOX_SIZE, allowed_updates=[UpdateType.MESSAGE]
            )
            self.inbox.extend(
                [update.message for update in new_updates if update.message]
            )
        message_data = self.inbox.popleft()
        incoming_message = self.create_incoming_message(message_data)
        return incoming_message

    async def send_message(self, message: Message) -> None:
        await self.telegram_bot.send_message(
            message.chat_id,
            message.message_text or "",
        )
