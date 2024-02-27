# flake8: noqa: F401

from oaiapi_teleproxy.telegram.experiments import (
    agr_main,
    ptb_main,
    tbt_main,
    ttn_main,
)


def launch_telegram_bot() -> None:
    ttn_main()
