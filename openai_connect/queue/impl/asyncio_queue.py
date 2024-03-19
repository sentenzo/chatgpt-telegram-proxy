import asyncio

from ..queue import Message, Queue


class AsyncIoQueue(Queue):
    def __init__(self) -> None:
        self.queues: dict[str | None, asyncio.Queue[Message]] = {}

    async def put(self, message: Message, topic: str | None = None) -> None:
        if topic not in self.queues:
            self.queues[topic] = asyncio.Queue()
        queue = self.queues[topic]
        await queue.put(message)

    async def get(self, topic: str | None = None) -> Message:
        if topic not in self.queues:
            self.queues[topic] = asyncio.Queue()
        queue = self.queues[topic]
        message = await queue.get()
        return message
