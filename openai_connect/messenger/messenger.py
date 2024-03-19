from abc import ABC, abstractmethod

from openai_connect import Message


class Messenger(ABC):
    @abstractmethod
    async def receive_message(self) -> Message:
        pass

    @abstractmethod
    async def send_message(self, message: Message) -> None:
        pass
