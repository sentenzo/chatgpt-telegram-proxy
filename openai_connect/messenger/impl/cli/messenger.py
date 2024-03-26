import asyncio
from datetime import datetime

from openai_connect.message import Message, MessageType
from openai_connect.messenger import Messenger


class CliMessenger(Messenger):
    def __init__(self) -> None:
        self.message_counter = 0

    async def receive_message(self) -> Message:
        input_text = await asyncio.to_thread(input, "[User]: ")
        self.message_counter += 1
        return Message(
            created_at=int(datetime.now().timestamp()),
            message_type=MessageType.INCOMING,
            chat_id="std_io",
            user_id="user",
            message_id=str(self.message_counter),
            message_text=input_text,
        )

    async def send_message(self, message: Message) -> None:
        print(f"[AI]: {message.message_text}")
