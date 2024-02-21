import json
def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

states = read_json('json/state.json')
country_data = read_json('json/countries.json')
cities_data = read_json('json/cities.json')


# from country to cities
def list_cities(country_name= None):
    response_data = []
    state_data = []

    if country_name is not None:
        for country in country_data:
            if country["name"] == country_name:
                data = country
                id = data['id']
                for state in states:
                    if state["country"] == str(id):
                        state_id = state['id']
                        for city in cities_data:
                            if city['state'] == str(state_id):
                                state_data.append(city)
                        response = {
                            'state': state['name'],
                            'sate_id': state['id'],
                            'cities': state_data
                        }
                        state_data = []
                        response_data.append(response)
                # with open('output.json', 'w') as json_file:
                #     json.dump(response_data, json_file, indent=2)
                return response_data
        data = {'country': 'Invalid Country Name'}
        return data
    else:
        return 'Please Provide Valid Input'

# print(list_cities("Pakistan"))


# from state to cities
def list_state_cities(state_name= None):
    response_data = []
    state_data = []

    if state_name is not None:
        for state in states:
            if state['name'] == state_name:
                for city in cities_data:
                    if city['state'] == str(state['id']):
                        state_data.append(city)
                response = {
                    'state': state['name'],
                    'sate_id': state['id'],
                    'cities': state_data
                }
                return response

# print(list_state_cities("Punjab"))