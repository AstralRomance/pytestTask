import itertools
import requests

SW_API_BASE_LINK = 'https://swapi.dev/api'

def get_people_list():
    all_people = []
    for page in itertools.count(1):
        swapi_link = ''.join((SW_API_BASE_LINK,f'/people/?page={page}'))
        swapi_request = requests.get(swapi_link)
        if swapi_request.status_code == 404:
            break
        all_people.extend(swapi_request.json()['results'])
    return all_people