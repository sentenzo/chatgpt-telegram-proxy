import os

from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY", default="")
BASE_URL = os.environ.get("OPENAI_API_BASE_URL", default="")
DEFAULT_MODEL = os.environ.get("OPENAI_API_DEFAULT_MODEL", default="")


def check_openai() -> None:
    client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
    question = "What is the purpose of your visit to the United States?"

    completion = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "user", "content": question},
        ],
        temperature=0.7,
        stop="### ",
        max_tokens=500,
    )

    print(completion.choices[0].message.content)
