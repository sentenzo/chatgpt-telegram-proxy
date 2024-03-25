from asyncio import PriorityQueue as AQueue

from ..queue import Queue


class AsyncIoQueue(AQueue, Queue):
    pass
