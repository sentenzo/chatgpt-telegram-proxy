from abc import ABC, abstractmethod
from collections.abc import Hashable
from dataclasses import dataclass


@dataclass
class Message(ABC):
    chat_id: Hashable
    user_id: Hashable
    command_id: Hashable | None
    raw_text: str | None

    @abstractmethod
    def to_text(self) -> str:
        pass
