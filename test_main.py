import pytest
import requests
import itertools

class TestSWApi:
    SW_API_BASE_LINK = 'https://swapi.dev/api'

    # TASK 1
    @pytest.fixture()
    def get_all_people(self):
        all_people = []
        for page in itertools.count(1):
            swapi_link = ''.join((self.SW_API_BASE_LINK,f'/people/?page={page}'))
            swapi_request = requests.get(swapi_link)
            if swapi_request.status_code == 404:
                break
            all_people.extend(swapi_request.json()['results'])
        return all_people

    @pytest.fixture()
    def get_different_case_names(self):
        return ['LUKE SKYWALKER', 'Luke Skywalker', 'luke skywalker', 'LuKe SkYwAlKeR']

    #TASK 7
    @pytest.fixture()
    def get_people_object_schema(self):
        request_link = ''.join((self.SW_API_BASE_LINK, '/people/schema'))
        return requests.get(request_link).json()['required']

    #TASK 2
    def test_count(self, get_all_people):
        swapi_link = ''.join((self.SW_API_BASE_LINK, f'/people'))
        num_of_people = requests.get(swapi_link).json()['count']
        assert len(get_all_people) == num_of_people

    #TASK 3
    def test_unique_names(self, get_all_people):
        names = [name['name'] for name in get_all_people]
        print(names)
        assert len(names) == len(set(names))

    #TASK 4
    def test_case_sensivity_valid_data(self, get_different_case_names):
        responses = []
        for name in get_different_case_names:
            request_link = ''.join((self.SW_API_BASE_LINK, f'/people/?search={name}'))
            responses.append(requests.get(request_link).status_code)
        assert all(200==response_code for response_code in responses)

    def test_case_sensivity_correct_data(self, get_different_case_names):
        correct_name = 'Luke Skywalker'
        requested_names = []
        for name in get_different_case_names:
            request_link = ''.join((self.SW_API_BASE_LINK, f'/people/?search={name}'))
            requested_names = [i['name'] for i in requests.get(request_link).json()['results']]
        assert all(correct_name==name for name in requested_names)

    #TASK 5
    def test_zero_page_validate(self):
        request_link = ''.join((self.SW_API_BASE_LINK,'/people/?page=0'))
        swapi_request = requests.get(request_link)
        assert swapi_request.status_code == 404

    #TASK 6
    @pytest.mark.parametrize('name, number',
                            [('Skywalker', 3),
                            ('Vader', 1),
                            ('Darth', 2)])
    def test_character_number(self, name, number):
        request_link = ''.join((self.SW_API_BASE_LINK, f'/people/?search={name}'))
        swapi_request = requests.get(request_link)
        assert swapi_request.json()['count'] == number

    #TASK 8
    def test_check_people_schema(self, get_all_people, get_people_object_schema):
        is_valid = []
        for people in get_all_people:
            is_valid.append(all(field in people for field in get_people_object_schema)) 
        assert all(schema==True for schema in is_valid)
