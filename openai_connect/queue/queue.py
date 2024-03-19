from abc import ABC, abstractmethod

from openai_connect import Message


class Queue(ABC):
    @abstractmethod
    async def put(self, message: Message) -> None:
        pass

    @abstractmethod
    async def get(self) -> Message:
        pass
