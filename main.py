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




def parser_cmd_args():
    """Parser information add information to func"""
    parser = argparse.ArgumentParser(description="launch_id for SPACE_X API, you can add if you need specific launch")
    parser.add_argument(
        "launch_id",
        type=str,
        default="latest",
        help="it must be 'str', for example: '5eb87d42ffd86e000604b384',"
             " you can find launch_id on the link: https://github.com/r-spacex/SpaceX-API/tree/master/docs/launches",
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


def main():
    env = Env()
    env.read_env()
    nasa_key = env.str("NASA_KEY")
    args = parser_cmd_args()
    launch_id = args.launch_id
    download_photos(fetch_spacex_launch(launch_id), "images/space_x_photos/")
    download_photos(fetch_nasa_apod(nasa_key), "images/nasa_apod_photos/")
    download_photos(
        fetch_nasa_epic(nasa_key),
        "images/nasa_epic_photos/",
        {"api_key": nasa_key}
    )
    change_picture_size()


if __name__ == "__main__":
    main()
