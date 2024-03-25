from abc import ABC, abstractmethod

from openai_connect import Message


class Queue(ABC):
    @abstractmethod
    async def put(self, message: Message) -> None:
        """Put an item into the queue."""
        pass

    @abstractmethod
    async def get(self) -> Message:
        """Remove and return an item from the queue."""
        pass

    @abstractmethod
    def qsize(self) -> int:
        """Number of items in the queue."""
        pass
