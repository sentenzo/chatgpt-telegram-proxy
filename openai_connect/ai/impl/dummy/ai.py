from datetime import datetime
from typing import AsyncGenerator

from openai_connect.ai import Ai
from openai_connect.message import Message, MessageType


class DummyAi(Ai):
    async def reply(
        self, message: Message, stream: bool = False
    ) -> AsyncGenerator[Message, None]:
        yield Message(
            int(datetime.now().timestamp()),
            MessageType.OUTGOING,
            chat_id=message.chat_id,
            user_id=f"assistant-{message.chat_id}",
            message_id=None,
            message_text=message.message_text,
        )
