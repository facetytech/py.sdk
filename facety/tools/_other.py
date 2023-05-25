import requests
import json


# Global variable to store the cached value of the meta.json file.
META: dict | None = None


def meta() -> dict:
    '''Returns the configuration of Facety's services.

    Returns:
        Configuration as a dictionary.
    '''

    global META

    if META is not None:
        return META

    headers = {'User-Agent': 'Facety/Python'}
    response = requests.get('https://static.facety.tech/meta.json', headers=headers)
    META = json.loads(response.text)

    return META
