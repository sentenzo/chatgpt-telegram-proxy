from openai_connect.message import Message, MessageType

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

MESSAGES = [Message(**kwarg) for kwarg in CORRECT_MESSAGE_KWARGS]

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
