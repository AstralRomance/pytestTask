import pytest
import requests
import itertools
import string
import json

SW_API_BASE_LINK = 'https://swapi.dev/api'

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

#TASK 7
@pytest.fixture()
def get_people_object_schema():
    request_link = ''.join((SW_API_BASE_LINK, '/people/schema'))
    return requests.get(request_link).json()['required']

#TASK 9
@pytest.fixture()
def people_search(search_parameters):
    swapi_link = ''.join((SW_API_BASE_LINK, '/people/', search_parameters))
    swapi_request = requests.get(swapi_link)
    return swapi_request.json()

#TASK 10
def symbol_return_test():
    symbols = [lt for lt in string.ascii_lowercase]
    symbols.extend([str(n) for n in range(10)])
    symbols.append('')
    api_sections = [''.join((section, '?search=')) for section in ['/people/', '/films/', '/starships/', '/vehicles/', '/species/', 'planets']]
    api_requests = [''.join(parameter) for parameter in itertools.product(api_sections, symbols)]
    api_requests = [''.join((SW_API_BASE_LINK, parameter)) for parameter in api_requests]
    return api_requests

#TASK 2
def test_count(get_all_people):
    swapi_link = ''.join((SW_API_BASE_LINK, f'/people'))
    num_of_people = requests.get(swapi_link).json()['count']
    assert len(get_all_people) == num_of_people

#TASK 3
def test_unique_names(get_all_people):
    names = [name['name'] for name in get_all_people]
    print(names)
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
    assert all(schema==True for schema in is_valid)

#TASK 10
@pytest.mark.parametrize('request_link', symbol_return_test())
def test_symbol(request_link):
    swapi_request = requests.get(request_link)
    try:
        if request_link[-1] in ['0', '6', '9']:
            assert int(swapi_request.json()['count']) == 0
        else:
            assert int(swapi_request.json()['count']) >= 1
    except json.JSONDecodeError:
        print('REQUEST TO ROOT API SECTIONS HAS NO COUNT KEY')

#TASK 11
