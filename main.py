import requests
from pathlib import Path
from itertools import islice
from os.path import splitext
from urllib.parse import urlparse, unquote


def fetch_spacex_last_launch(image_urls: list, path: str):
    """Creates a file for every picture and safe in folder"""
    Path(path).mkdir(parents=True, exist_ok=True)
    for image_number, url in islice(enumerate(image_urls, 1), 0, 5):
        filename = f"{image_number}.jpeg"
        response = requests.get(url)
        response.raise_for_status()

        with open(f"{path}{filename}", "wb") as file:
            file.write(response.content)
    return


def get_links(url: str) -> list:
    """Get list of image urls from the API"""
    payload = {"id": "latest"}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    launch = response.json()
    image_urls = []
    for images in launch:
        image = images['links']['flickr']['original']
        if image:
            image_urls.extend(image)
    return image_urls


def get_file_extension(url_photo: str) -> str:
    """Return the file extension."""
    parse_result_path = urlparse(unquote(url_photo)).path
    root, extension = splitext(parse_result_path)
    return extension


if __name__ == '__main__':
    API_URL_SPACE_X = "https://api.spacexdata.com/v5/launches/"
    fetch_spacex_last_launch(get_links(API_URL_SPACE_X), "images/")
    url_photo = "https://example.com/txt/hello%20world.txt?v=9#python"
    print(get_file_extension(url_photo))

