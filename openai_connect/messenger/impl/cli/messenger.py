import asyncio

from openai_connect.message import Message, MessageType
from openai_connect.messenger import Messenger

CHAT_ID = "std_io"
USER_ID = "user"


class CliMessenger(Messenger):
    def __init__(self) -> None:
        self.message_counter = 0

    async def receive_message(self) -> Message:
        input_text = await asyncio.to_thread(input, "[User]: ")
        self.message_counter += 1
        return Message(
            type_=MessageType.INCOMING,
            chat_id=CHAT_ID,
            user_id=USER_ID,
            message_id=str(self.message_counter),
            message_text=input_text,
        )

    async def send_message(self, message: Message) -> None:
        assert message.chat_id == CHAT_ID
        assert message.user_id == USER_ID
        assert message.message_id is None
        print(f"[AI]: {message.message_text}")
