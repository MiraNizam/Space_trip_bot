import datetime

import requests


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
