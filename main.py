import argparse
import os
from itertools import islice
from os.path import splitext
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests
from environs import Env
from PIL import Image

from fetch_nasa_apod_photos import fetch_nasa_apod
from fetch_nasa_epic_photos import fetch_nasa_epic
from fetch_spacex_photos import fetch_spacex_launch

env = Env()
env.read_env()


def parser_cmd_args():
    """Parser information add information to func"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "launch_id",
        type=str,
        default="latest",
        help="Input the launch_id, if you miss it, func will use 'latest' launch",
    )
    return parser.parse_args()


def get_file_extension(url_photo: str) -> str:
    """Return the file extension."""
    parse_result_path = urlparse(unquote(url_photo)).path
    root, extension = splitext(parse_result_path)
    return extension


def download_photos(image_urls: list, path: str, params: dict = {}) -> None:
    """Download photos and safe them in folder"""
    Path(path).mkdir(parents=True, exist_ok=True)
    for image_number, url in islice(enumerate(image_urls, 1), 0, 25):
        filename = f"{image_number}{get_file_extension(url)}"
        response = requests.get(url, params=params)
        response.raise_for_status()

        with open(f"{path}{filename}", "wb") as file:
            file.write(response.content)


def change_picture_size(path: str = "images/"):
    """Reduces photos while maintaining aspect ratio."""
    for root, dir, files in os.walk(path):
        for picture in files:
            with Image.open(f"{root}/{picture}") as file:
                file.thumbnail((1280, 1280))
                file.save(f"{root}/{picture}")


if __name__ == "__main__":
    args = parser_cmd_args()
    launch_id = args.launch_id
    NASA_KEY = env.str("NASA_KEY")
    download_photos(fetch_spacex_launch(launch_id), "images/space_x_photos/")
    download_photos(fetch_nasa_apod(NASA_KEY), "images/nasa_apod_photos/")
    download_photos(
        fetch_nasa_epic(NASA_KEY),
        "images/nasa_epic_photos/",
        {"api_key": NASA_KEY}
    )
    change_picture_size()
