import pytest
import requests

SW_API_BASE_LINK = 'https://swapi.dev/api'

# TASK 1
@pytest.fixture()
def get_all_people():
    request_link = ''.join(SW_API_BASE_LINK,'/people')
    swapi_request = requests.get(request_link)
    return swapi_request.json()['results']

@pytest.fixture()
def get_different_case_names():
    return ['LUKE SKYWALKER', 'Luke Skywalker', 'luke skywalker', 'LuKe SkYwAlKeR']

#TASK 7
@pytest.fixture()
def get_people_object_schema():
    request_link = ''.join(SW_API_BASE_LINK, '/people/schema')
    return requests.get(request_link)['required']

#TASK 2
def count_test(get_all_people):
    request_link = ''.join(SW_API_BASE_LINK,'/people')
    swapi_request = requests.get(request_link)
    assert len(get_all_people) == swapi_request.json()['count']

#TASK 3
def unique_names_test(get_all_people):
    names = [name for name in get_all_people['name']]
    assert len(names) == len(set(names))

#TASK 4
def case_sensivity_valid_data_test(get_different_case_names):
    responses = []
    for name in get_different_case_names:
        request_link = ''.join(SW_API_BASE_LINK, f'/people/?search={name}')
        responses.append(requests.get(request_link).status_code)
    assert all(200==response_code for response_code in responses)

def case_sensivity_correct_data_test(get_different_case_names):
    correct_name = 'Luke Skywalker'
    requested_names = []
    for name in get_different_case_names:
        request_link = ''.join(SW_API_BASE_LINK, f'/people/?search={name}')
        requested_namess.append(requests.get(request_link).json()['results']['name'])
    assert all(correct_name==name for name in requested_name)

#TASK 5
def zero_page_validate_test():
    request_link = ''.join(SW_API_BASE_LINK,'/people/?page=0')
    swapi_request = requests.get(request_link)
    assert swapi_request.status_code == 404

#TASK 6
@pytest.mark.parametrize('name, number',
                        [('Skywalker', 3),
                         ('Vader', 1),
                         ('Darth', 2)])
def character_number_test(name, number):
    request_link = ''.join(SW_API_BASE_LINK, f'/people/?search={name}')
    swapi_request = requests.get(request_link)
    assert swapi_request.json()['count'] == number

#TASK 8
def check_people_schema_test(get_all_people, get_people_object_schema):
    is_valid = []
    for people in get_all_people:
        is_valid.append(all(field in people for field in get_people_object_schema)) 
    assert all(schema==True for schema in is_valid)
