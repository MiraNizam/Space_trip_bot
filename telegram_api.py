import argparse
import os
import os.path
import time

import telegram
from environs import Env


def send_to_bot(token: str, chat_id: str, sleep: int, path: str = "images/") -> None:
    """send photos to telegram by one piece with the specified interval"""
    bot = telegram.Bot(token=token)
    while True:
        for root, dir, files in os.walk(path):
            for picture in files:
                with open(f"{root}/{picture}", "rb") as file:
                    bot.send_photo(chat_id=chat_id, photo=file)
                time.sleep(sleep)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "interval_in_seconds",
        type=int,
        default=14400,
        help="you can specify the interval in seconds to publish photos, default is 14440",
    )
    namespace = parser.parse_args()

    sleep = int(namespace.interval_in_seconds)
    token = env.str("TG_TOKEN")
    chat_id = env.str("TG_CHAT_ID")
    send_to_bot(token, chat_id, sleep)
