from abc import ABC, abstractmethod

from .message import Message
from .queue import Queue


class Communicator(ABC):
    @property
    @abstractmethod
    def queue(self) -> Queue:
        pass

    async def get_next_request(self) -> Message:
        return await self.queue.get_next_request()

    @abstractmethod
    async def send_response(self, response: Message) -> None:
        pass
