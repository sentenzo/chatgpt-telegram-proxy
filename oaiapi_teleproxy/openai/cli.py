import os

from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

API_KEY = os.environ.get("OPENAI_API_KEY", default="")
BASE_URL = os.environ.get("OPENAI_API_BASE_URL", default="")
DEFAULT_MODEL = os.environ.get("OPENAI_API_DEFAULT_MODEL", default="")
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

BOT_CAPTION = "[AI]: "
USER_CAPTION = "[User]: "


history: list[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": (
            "You are an intelligent assistant. You always provide "
            "well-reasoned answers that are both correct and helpful."
        ),
    },
    {
        "role": "user",
        "content": (
            "Hello, introduce yourself to someone opening "
            "this program for the first time. Be concise."
        ),
    },
]


def run_cli() -> None:
    try:
        while True:
            completion = client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=history,
                temperature=0.7,
                max_tokens=1000,
                stream=True,
            )
            bot_input: list[str] = []
            print(BOT_CAPTION, end="")
            for chunk in completion:
                text = chunk.choices[0].delta.content or ""
                print(text, end="", flush=True)
                bot_input.append(text)
            print()
            history.append(
                {
                    "role": "assistant",
                    "content": "".join(bot_input),
                }
            )
            user_input = input(USER_CAPTION)
            history.append({"role": "user", "content": user_input})
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    run_cli()
