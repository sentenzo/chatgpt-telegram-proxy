import asyncio

from pytest import CaptureFixture, MonkeyPatch

from openai_connect.messenger.impl import CliMessenger
from tests.unit.const import AWAIT_TIMEOUT, MESSAGES


def test_init() -> None:
    CliMessenger()


async def test_send_message(capfd: CaptureFixture[str]) -> None:
    msgr = CliMessenger()
    message = MESSAGES[0]
    await asyncio.wait_for(msgr.send_message(message), AWAIT_TIMEOUT)
    stdout, stderr = capfd.readouterr()
    assert stdout == f"[AI]: {message.message_text}\n"
    assert stderr == ""


async def test_receive_message(monkeypatch: MonkeyPatch) -> None:
    msgr = CliMessenger()
    message_text = "message_text"

    def my_input(prompt: str) -> str:
        assert prompt == "[User]: "
        return message_text

    monkeypatch.setattr("builtins.input", my_input)
    msg = await asyncio.wait_for(msgr.receive_message(), AWAIT_TIMEOUT)
    assert msg.message_text == message_text
