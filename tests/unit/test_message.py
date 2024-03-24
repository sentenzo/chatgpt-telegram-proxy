import json
from dataclasses import FrozenInstanceError, asdict

import pytest

from openai_connect.message import Message, MessageParsingError, MessageType

CORRECT_MESSAGE_PARAMETERS: dict[str, list] = {
    "created_at": [
        1600171844,
        -123,
        0,
    ],
    "message_type": [
        MessageType.INCOMING,
        MessageType.OUTGOING,
        MessageType.OUTGOING_APPEND,
        MessageType.UNKNOWN,
    ],
    "chat_id": ["-0qwerty", ""],
    "user_id": ["-0qwerty", "", None],
    "message_id": ["-0qwerty", "", None],
    "message_text": ["text '\"}{</div> ; -- DELETE TABLE Students;", "", None],
}

CORRECT_MESSAGE_KWARGS = [
    {
        "created_at": created_at,
        "message_type": message_type,
        "chat_id": chat_id,
        "user_id": user_id,
        "message_id": message_id,
        "message_text": message_text,
    }
    for created_at in CORRECT_MESSAGE_PARAMETERS["created_at"]
    for message_type in CORRECT_MESSAGE_PARAMETERS["message_type"]
    for chat_id in CORRECT_MESSAGE_PARAMETERS["chat_id"]
    for user_id in CORRECT_MESSAGE_PARAMETERS["user_id"]
    for message_id in CORRECT_MESSAGE_PARAMETERS["message_id"]
    for message_text in CORRECT_MESSAGE_PARAMETERS["message_text"]
]  # 3*4*2*3*3*3 == 648 variants

INCORRECT_MESSAGE_PARAMETERS: dict[str, list] = {
    "created_at": [
        None,
        "12",
        1600171844.0,
    ],
    "message_type": [
        MessageType.INCOMING,
        MessageType.OUTGOING,
        MessageType.OUTGOING_APPEND,
        MessageType.UNKNOWN,
    ],
    "chat_id": ["-0qwerty", ""],
    "user_id": ["-0qwerty", "", None],
    "message_id": ["-0qwerty", "", None],
    "message_text": ["text '\"}{</div> ; -- DELETE TABLE Students;", "", None],
}


def test_init() -> None:
    for message_kwarg in CORRECT_MESSAGE_KWARGS:
        Message(**message_kwarg)


def test_init_no_optionals() -> None:
    """checking absence of optional params"""
    message_kwarg = CORRECT_MESSAGE_KWARGS[0]
    del message_kwarg["user_id"]
    del message_kwarg["message_id"]
    del message_kwarg["message_text"]
    Message(**message_kwarg)


def test_immutability() -> None:
    message = Message(**CORRECT_MESSAGE_KWARGS[0])

    with pytest.raises(TypeError):
        message.some_new_attr = 123  # type: ignore

    with pytest.raises(FrozenInstanceError):
        message.chat_id = "123"  # type: ignore


def test_json_serialization() -> None:
    for message_kwarg in CORRECT_MESSAGE_KWARGS:
        message_before = Message(**message_kwarg)
        json_string = message_before.to_json()
        message_after = Message.from_json(json_string)
        assert message_before == message_after


def test_json_incorrect_serialization() -> None:
    message = Message(**CORRECT_MESSAGE_KWARGS[0])
    message_kwarg = asdict(message)
    assert json.dumps(message_kwarg) == message.to_json()

    with pytest.raises(MessageParsingError):
        message_kwarg_incorrect = message_kwarg.copy()
        message_kwarg_incorrect["message_type"] = "qwerty"
        json_string_incorrect = json.dumps(message_kwarg_incorrect)
        Message.from_json(json_string_incorrect)

    with pytest.raises(MessageParsingError):
        message_kwarg_incorrect = message_kwarg.copy()
        message_kwarg_incorrect["created_at"] = "2345-12-21"
        json_string_incorrect = json.dumps(message_kwarg_incorrect)
        Message.from_json(json_string_incorrect)
