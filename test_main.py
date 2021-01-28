import itertools
import string
import json
import datetime
import pytest
import requests
import dateutil.parser

from utility import SW_API_BASE_LINK
from utility import all_sections_requests, get_people_list

#TASK 2
def test_count(get_all_people):
    swapi_link = ''.join((SW_API_BASE_LINK, f'/people'))
    num_of_people = requests.get(swapi_link).json()['count']
    assert len(get_all_people) == num_of_people

#TASK 3
def test_unique_names(get_all_people):
    names = [name['name'] for name in get_all_people]
    assert len(names) == len(set(names))
#TASK 4
def test_case_sensivity_valid_data(get_different_case_names):
    responses = []
    for name in get_different_case_names:
        request_link = ''.join((SW_API_BASE_LINK, f'/people/?search={name}'))
        responses.append(requests.get(request_link).status_code)
    assert all(200==response_code for response_code in responses)

def test_case_sensivity_correct_data(get_different_case_names):
    correct_name = 'Luke Skywalker'
    requested_names = []
    for name in get_different_case_names:
        request_link = ''.join((SW_API_BASE_LINK, f'/people/?search={name}'))
        requested_names = [i['name'] for i in requests.get(request_link).json()['results']]
    assert all(correct_name==name for name in requested_names)

#TASK 5
def test_zero_page_validate():
    request_link = ''.join((SW_API_BASE_LINK,'/people/?page=0'))
    swapi_request = requests.get(request_link)
    assert swapi_request.status_code == 404

#TASK 6
@pytest.mark.parametrize('name, number',
                        [('Skywalker', 3),
                        ('Vader', 1),
                        ('Darth', 2)])
def test_character_number(name, number):
    request_link = ''.join((SW_API_BASE_LINK, f'/people/?search={name}'))
    swapi_request = requests.get(request_link)
    assert swapi_request.json()['count'] == number

#TASK 8
def test_check_people_schema(get_all_people, get_people_object_schema):
    is_valid = []
    for people in get_all_people:
        is_valid.append(all(field in people for field in get_people_object_schema)) 
    assert all(schema is True for schema in is_valid)

#TASK 10
@pytest.mark.parametrize('request_link', all_sections_requests())
def test_symbol(request_link):
    swapi_request = requests.get(request_link)
    if swapi_request.status_code == 200:
        if request_link[-1] in ['0', '6', '9']:
            assert int(swapi_request.json()['count']) == 0
        else:
            assert int(swapi_request.json()['count']) >= 1
    else:
        pytest.fail(f'Request with {swapi_request.status_code} code')

#TASK 11
@pytest.mark.parametrize('character', get_people_list())
def test_valid_created_time(character):
    try:
        assert isinstance(dateutil.parser.parse(character['created']), datetime.datetime)
    except dateutil.parser.ParserError:
        pytest.fail('Date create parsing failed (Invalid date)')

@pytest.mark.parametrize('character', get_people_list())
def test_valid_edited_time(character):
    try:
        assert isinstance(dateutil.parser.parse(character['edited']), datetime.datetime)
    except dateutil.parser.ParserError:
        pytest.fail('Date edited parsing failed (invalid or empty date)')

@pytest.mark.parametrize('character', get_people_list())
def test_films_valid_link(character):
    valid_links = []
    for link in character['films']:
        valid_links.append(requests.get(link).status_code == 200)
    assert all([is_valid is True for is_valid in valid_links])

@pytest.mark.parametrize('character', get_people_list())
def test_homeworld_valid_link(character):
    assert requests.get(character['homeworld']).status_code == 200

@pytest.mark.parametrize('character', get_people_list())
def test_species_valid_link(character):
    valid_links = []
    for link in character['species']:
        valid_links.append(requests.get(link).status_code == 200)
    assert all([is_valid is True for is_valid in valid_links])

#TASK 12
def test_people_wookiee_endpoints_response(get_people_wookiee_endpoints):
    valid_response = []
    for link in get_people_wookiee_endpoints:
        valid_response.append(requests.get(link).status_code == 200)
    assert all([is_valid is True for is_valid in valid_response])

def test_people_wookiee_endpoints_valid_json(get_people_wookiee_endpoints):
    valid_response = []
    for link in get_people_wookiee_endpoints:
        try:
            valid_response.append(isinstance(requests.get(link).json(),dict))
        except json.JSONDecodeError:
            valid_response.append(False)
    assert all([is_valid is True for is_valid in valid_response])
