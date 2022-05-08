from typing import Union, List

import requests


def search_movie_api(url: str, default_response: Union[List, None] = None):
    response = requests.get(url)
    if response.status_code == 200:
        json_response = response.json()['Search']
        return json_response
    return default_response
