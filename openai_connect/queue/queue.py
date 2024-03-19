from abc import ABC, abstractmethod

from openai_connect import Message


class Queue(ABC):
    @abstractmethod
    async def put(self, message: Message, topic: str | None = None) -> None:
        pass

    @abstractmethod
    async def get(self, topic: str | None = None) -> Message:
        pass
