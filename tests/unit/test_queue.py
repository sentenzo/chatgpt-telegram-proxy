import asyncio

import pytest

from openai_connect.queue import Queue
from openai_connect.queue.impl import AsyncIoQueue
from tests.unit.const import AWAIT_TIMEOUT, MESSAGES


async def put_messages(q: Queue) -> None:
    for message in MESSAGES:
        await q.put(message)


async def test_init() -> None:
    AsyncIoQueue()


async def test_put() -> None:
    queue = AsyncIoQueue()

    await asyncio.wait_for(
        put_messages(queue), AWAIT_TIMEOUT
    )  # can fail with TimeoutError


async def test_get() -> None:
    queue = AsyncIoQueue()

    message_in = MESSAGES[0]
    await queue.put(message_in)
    message_out = await asyncio.wait_for(queue.get(), AWAIT_TIMEOUT)
    assert message_in == message_out

    await put_messages(queue)

    async def get_messages(n: int) -> None:
        for _ in range(n):
            await queue.get()

    await asyncio.wait_for(get_messages(len(MESSAGES)), AWAIT_TIMEOUT)

    with pytest.raises(asyncio.TimeoutError):
        # no messages in the queue now
        await asyncio.wait_for(queue.get(), AWAIT_TIMEOUT)
