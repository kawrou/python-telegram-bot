import requests


def fetch_cat_photo(colour: str) -> str:
    api_url = f"https://cataas.com/cat/{colour}"
    response = requests.get(api_url)
    if response.status_code == 200:
        # data = response.json()
        # return data.get("photo_url", None)
        return api_url
    else:
        return None
