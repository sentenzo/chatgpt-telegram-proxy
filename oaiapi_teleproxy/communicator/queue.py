from abc import ABC, abstractmethod
from asyncio import Queue as AQue

from .message import Message


class Queue(ABC):
    @abstractmethod
    async def put_request(self, message: Message) -> None:
        pass

    @abstractmethod
    async def put_reesponse(self, message: Message) -> None:
        pass

    @abstractmethod
    async def get_next_request(self) -> Message:
        pass

    @abstractmethod
    async def get_next_reesponse(self) -> Message:
        pass


class AsyncIoQueue(Queue):
    def __init__(self) -> None:
        self.request_queue: AQue[Message] = AQue()
        self.reesponse_queue: AQue[Message] = AQue()

    async def put_request(self, message: Message) -> None:
        await self.request_queue.put(message)

    async def put_reesponse(self, message: Message) -> None:
        await self.reesponse_queue.put(message)

    async def get_next_request(self) -> Message:
        return await self.request_queue.get()

    async def get_next_reesponse(self) -> Message:
        return await self.reesponse_queue.get()
