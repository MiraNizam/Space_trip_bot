import requests
from pathlib import Path
from itertools import islice
from os.path import splitext
from urllib.parse import urlparse, unquote
import datetime
from environs import Env

env = Env()
env.read_env()


def get_file_extension(url_photo: str) -> str:
    """Return the file extension."""
    parse_result_path = urlparse(unquote(url_photo)).path
    root, extension = splitext(parse_result_path)
    return extension


def fetch_spacex_last_launch() -> list:
    """Get list of image urls from the SpaceX API request"""
    spacex_api_launches = "https://api.spacexdata.com/v5/launches/"
    payload = {"id": "latest"}
    response = requests.get(spacex_api_launches, params=payload)
    response.raise_for_status()
    launch = response.json()
    image_urls = []
    for images in launch:
        image = images['links']['flickr']['original']
        if image:
            image_urls.extend(image)
    return image_urls


def fetch_nasa_apod(api_key: str, limit: int = 5) -> list:
    """Get list of image urls from the the NASA APOD API"""
    nasa_api_apod = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key,
              "count": limit}
    response = requests.get(nasa_api_apod, params=params)
    response.raise_for_status()
    apod_photos = response.json()
    image_urls = []

    for photo in apod_photos:
        image = photo['hdurl']
        image_urls.append(image)
    return image_urls


def fetch_nasa_epic(api_key: str) -> list:
    """Get list of image urls from the NASA EPIC API"""
    nasa_api_epic = "https://api.nasa.gov/EPIC/api/natural/images"
    nasa_api_epic_photo = "https://api.nasa.gov/EPIC/archive/natural/"
    params = {"api_key": api_key}
    response = requests.get(nasa_api_epic, params=params)
    response.raise_for_status()
    photo_parameters = response.json()
    image_urls = []

    for parameter in photo_parameters:
        date = datetime.datetime.fromisoformat(parameter["date"]).strftime("%Y/%m/%d")
        date_path = f"{date}/png/"
        name = f'{parameter["image"]}.png'
        epic_url = f"{nasa_api_epic_photo}{date_path}{name}"
        image_urls.append(epic_url)
    return image_urls


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


