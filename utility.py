import string
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

def all_sections_requests():
    symbols = list(f'{string.ascii_lowercase}{string.digits} ')
    api_sections = [''.join((section, '?search=')) for section in ['/people/', '/films/', '/starships/', '/vehicles/', '/species/', 'planets']]
    api_requests = [''.join(parameter) for parameter in itertools.product(api_sections, symbols)]
    api_requests = [''.join((SW_API_BASE_LINK, parameter)) for parameter in api_requests]
    return api_requests
