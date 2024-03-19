import json
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum

from openai_connect.exception import OpenAiConnectException


class MessageParsingError(OpenAiConnectException):
    pass


class MessageType(str, Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"
    UNKNOWN = "unknown"


class JsonBijectable(ABC):
    @abstractmethod
    def to_json() -> str:
        pass

    @staticmethod
    @abstractmethod
    def from_json(json_str: str) -> "JsonBijectable":
        pass


@dataclass(frozen=True, slots=True)
class Message(JsonBijectable):
    type_: MessageType
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
            obj["type_"] = MessageType(obj["type_"])
            return Message(**obj)
        except TypeError as e:
            raise MessageParsingError(
                "Failed to create Message object from JSON"
            ) from e
