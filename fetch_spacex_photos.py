import requests


def fetch_spacex_launch(launch_id: str="latest") -> list:
    """Get list of image urls from the SpaceX API request"""
    spacex_api_launches = "https://api.spacexdata.com/v5/launches/"
    payload = {"id": launch_id}
    response = requests.get(spacex_api_launches, params=payload)
    response.raise_for_status()
    links = response.json()
    image_urls = []
    for images in links:
        image = images['links']['flickr']['original']
        if image:
            image_urls.extend(image)
    return image_urls
