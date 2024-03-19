from abc import ABC, abstractmethod

from openai_connect import Message


class Messenger(ABC):
    @abstractmethod
    async def receive_message() -> Message:
        pass

    @abstractmethod
    async def send_message(message: Message) -> None:
        pass
