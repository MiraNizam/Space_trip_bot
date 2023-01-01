import requests


def fetch_nasa_apod(api_key: str, limit: int = 5) -> list:
    """Get list of image urls from the NASA APOD API"""
    nasa_api_apod = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key,
              "count": limit}
    response = requests.get(nasa_api_apod, params=params)
    response.raise_for_status()
    apod_photos = response.json()
    image_urls = [photo['hdurl'] for photo in apod_photos]
    return image_urls


