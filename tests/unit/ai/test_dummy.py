import asyncio

from openai_connect.ai.impl.dummy.ai import DummyAi

from tests.unit.const import AWAIT_TIMEOUT, MESSAGES


def test_init() -> None:
    DummyAi()


async def test_reply() -> None:
    ai = DummyAi()
    for message in MESSAGES:
        replies = await asyncio.wait_for(
            ai.reply_as_list(message), AWAIT_TIMEOUT
        )
        assert len(replies) == 1
        reply = replies[0]
        assert reply.message_text == message.message_text
