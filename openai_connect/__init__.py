from dotenv import load_dotenv

from .exception import OpenAiConnectException
from .message import Message, MessageType

load_dotenv(".env.openaiapi")
load_dotenv(".env.telegram")

__all__ = ["Message", "MessageType", "OpenAiConnectException"]
