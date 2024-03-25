import asyncio
from typing import Awaitable

from openai_connect.ai import Ai
from openai_connect.messenger import Messenger
from openai_connect.queue import Queue

TIMEOUT = 1


class Bot:
    def __init__(
        self,
        messenger: Messenger,
        mq_user: Queue,
        mq_ai: Queue,
        ai: Ai,
    ) -> None:
        self.messenger = messenger
        self.mq_user = mq_user
        self.mq_ai = mq_ai
        self.ai = ai
        self.stop_event = asyncio.Event()

    async def _receive_next_request_from_user(self) -> None:
        # stage 1
        new_request = await self.messenger.receive_message()
        await self.mq_user.put(new_request)

    async def _generate_next_response_from_ai(self) -> None:
        # stage 2
        new_request = await self.mq_user.get()
        async for new_response in self.ai.reply(new_request):
            await self.mq_ai.put(new_response)

    async def _send_next_response_to_user(self) -> None:
        # stage 3
        new_response = await self.mq_ai.get()
        await self.messenger.send_message(new_response)

    async def _repeat_until_bot_stopped(self, awaitable: Awaitable) -> None:
        while True:
            if self.stop_event.is_set():
                break
            await asyncio.wait_for(awaitable, TIMEOUT)

    async def launch(self) -> None:
        task_1 = self._repeat_until_bot_stopped(
            self._receive_next_request_from_user()
        )
        task_2 = self._repeat_until_bot_stopped(
            self._generate_next_response_from_ai()
        )
        task_3 = self._repeat_until_bot_stopped(
            self._send_next_response_to_user()
        )
        await asyncio.gather(task_1, task_2, task_3)

    def stop(self) -> None:
        self.stop_event.set()
