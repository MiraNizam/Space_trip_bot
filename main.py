import requests
from pathlib import Path
from itertools import islice
from os.path import splitext
from urllib.parse import urlparse, unquote
from environs import Env

from fetch_spacex_photos import fetch_spacex_last_launch
from fetch_nasa_apod_photos import fetch_nasa_apod
from fetch_nasa_epic_photos import fetch_nasa_epic

env = Env()
env.read_env()


def get_file_extension(url_photo: str) -> str:
    """Return the file extension."""
    parse_result_path = urlparse(unquote(url_photo)).path
    root, extension = splitext(parse_result_path)
    return extension


def download_photos(image_urls: list, path: str, params: dict = {}) -> None:
    """Download photos and safe them in folder"""
    Path(path).mkdir(parents=True, exist_ok=True)
    for image_number, url in islice(enumerate(image_urls, 1), 0, 5):
        filename = f"{image_number}{get_file_extension(url)}"
        response = requests.get(url, params=params)
        response.raise_for_status()

        with open(f"{path}{filename}", "wb") as file:
            file.write(response.content)


if __name__ == '__main__':
    download_photos(fetch_spacex_last_launch(), "images/space_x_photos/")
    NASA_KEY = env.str("NASA_KEY")
    download_photos(fetch_nasa_apod(NASA_KEY), "images/nasa_apod_photos/")
    download_photos(fetch_nasa_epic(NASA_KEY), "images/nasa_epic_photos/", {"api_key": NASA_KEY})


