import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum
from functools import total_ordering

from openai_connect.exception import OpenAiConnectException


class MessageParsingError(OpenAiConnectException):
    pass


class MessageType(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    OUTGOING_APPEND = "outgoing_append"
    UNKNOWN = "unknown"


class JsonBijectable(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json(json_str: str) -> "JsonBijectable":
        pass


@total_ordering
@dataclass(frozen=True, slots=True)
class Message(JsonBijectable):
    created_at: int  # UNIX time
    message_type: MessageType
    chat_id: str
    user_id: str | None = None
    message_id: str | None = None
    message_text: str | None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @staticmethod
    def from_json(json_str: str) -> "Message":
        try:
            obj = json.loads(json_str)
            obj["created_at"] = int(obj["created_at"])
            obj["message_type"] = MessageType(obj["message_type"])
            return Message(**obj)
        except (TypeError, ValueError) as e:
            raise MessageParsingError(
                "Failed to create Message object from JSON"
            ) from e

    def _sorting_key(self) -> tuple:
        return (
            self.created_at,
            self.chat_id,
            self.message_id,
            self.user_id,
            self.message_text,
            self.message_type,
        )

    def __lt__(self, other: "Message") -> bool:
        return self._sorting_key() < other._sorting_key()
