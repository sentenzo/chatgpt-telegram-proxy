import json
from dataclasses import FrozenInstanceError, asdict
from typing import Any

import pytest

from openai_connect.message import Message, MessageParsingError

from .const import CORRECT_MESSAGE_KWARGS, MESSAGES


def update_message(
    old_message: Message, new_kwargs: dict[str, Any]
) -> Message:
    kwargs = asdict(old_message)
    kwargs.update(**new_kwargs)
    return Message(**kwargs)


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
    message = MESSAGES[0]

    with pytest.raises(TypeError):
        message.some_new_attr = 123  # type: ignore

    with pytest.raises(FrozenInstanceError):
        message.chat_id = "123"  # type: ignore


def test_json_serialization() -> None:
    for message_before in MESSAGES:
        json_string = message_before.to_json()
        message_after = Message.from_json(json_string)
        assert message_before == message_after


def test_json_incorrect_serialization() -> None:
    message = MESSAGES[0]
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


def test_ordering() -> None:
    message_1, message_2, message_3 = MESSAGES[:3]
    message_1 = update_message(message_1, {"created_at": -14})
    message_2 = update_message(message_2, {"created_at": 8})
    message_3 = update_message(message_3, {"created_at": 42})
    assert message_1 < message_2 < message_3
    assert message_1 <= message_2 <= message_3
    assert message_3 > message_2 > message_1
    assert message_3 >= message_2 >= message_1

    message_1 = update_message(message_1, {"created_at": 8})
    assert message_2 < message_1 < message_3

    message_1 = update_message(message_1, asdict(message_2))
    assert message_1 <= message_2
    assert message_1 >= message_2
    assert message_1 == message_2


def test_sorting() -> None:
    messages = sorted(MESSAGES)
    for message in messages:
        assert message in MESSAGES
