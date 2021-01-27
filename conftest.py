import itertools

import pytest
import requests

from utility import SW_API_BASE_LINK

# TASK 1
@pytest.fixture()
def get_all_people():
    all_people = []
    for page in itertools.count(1):
        swapi_link = ''.join((SW_API_BASE_LINK,f'/people/?page={page}'))
        swapi_request = requests.get(swapi_link)
        if swapi_request.status_code == 404:
            break
        all_people.extend(swapi_request.json()['results'])
    return all_people

@pytest.fixture()
def get_different_case_names():
    return ['LUKE SKYWALKER', 'Luke Skywalker', 'luke skywalker', 'LuKe SkYwAlKeR']

@pytest.fixture()
def get_people_object_schema():
    request_link = ''.join((SW_API_BASE_LINK, '/people/schema'))
    return requests.get(request_link).json()['required']

@pytest.fixture()
def people_search(search_parameters):
    swapi_link = ''.join((SW_API_BASE_LINK, '/people/', search_parameters))
    swapi_request = requests.get(swapi_link)
    return swapi_request.json()

@pytest.fixture()
def get_people_wookiee_endpoints():
    return ['https://swapi.dev/api/people/?format=wookiee', 'https://swapi.dev/api/people/1/?format=wookiee', 'https://swapi.dev/api/people/schema/?format=wookiee']