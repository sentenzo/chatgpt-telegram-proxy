import asyncio

import pytest

from openai_connect.message import Message, MessageType
from openai_connect.queue import Queue
from openai_connect.queue.impl import AsyncIoQueue

TIMEOUT = 0.1


async def put_messages(q: Queue, n: int, topics: tuple = (None,)) -> None:
    for i in range(n):
        m_type = (
            MessageType.INCOMING,
            MessageType.OUTGOING,
            MessageType.UNKNOWN,
        )[i % 3]
        message = Message(123, m_type, "some_chat_id")
        topic = topics[i % len(topics)]
        await q.put(message, topic)


async def test_init() -> None:
    AsyncIoQueue()


async def test_put() -> None:
    queue = AsyncIoQueue()

    await asyncio.wait_for(
        put_messages(queue, 1000, (None, "a", "b", "c")), TIMEOUT
    )  # can fail with TimeoutError


async def test_get() -> None:
    queue = AsyncIoQueue()

    message_in = Message(
        -14, MessageType.INCOMING, "some_chat_id", message_text="qwerty"
    )
    await queue.put(message_in, "some_topic")
    message_out = await asyncio.wait_for(queue.get("some_topic"), TIMEOUT)
    assert message_in == message_out

    n = 100
    await put_messages(queue, n, topics=(None,))

    async def get_messages(k: int) -> None:
        for _ in range(k):
            await queue.get(None)

    await asyncio.wait_for(get_messages(n), TIMEOUT)

    with pytest.raises(asyncio.TimeoutError):
        # no messages in the queue now
        await asyncio.wait_for(queue.get(None), TIMEOUT)
