from abc import ABC, abstractmethod
from typing import AsyncGenerator

from openai_connect import Message, MessageType


class Ai(ABC):
    @abstractmethod
    async def reply(
        self, message: Message, stream: bool = False
    ) -> AsyncGenerator[Message, None]:
        yield Message(0, MessageType.UNKNOWN, "whatever")
        raise NotImplementedError()

    async def reply_as_list(
        self, message: Message, stream: bool = False
    ) -> list[Message]:
        responses = []
        async for reply in self.reply(message, stream):
            responses.append(reply)
        return responses
