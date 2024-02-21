import json
def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

states = read_json('json/state.json')
country_data = read_json('json/countries.json')

def validate_state(state_name=None):
    if state_name is not None:
        for state in states:
            if state["name"] == state_name:
                data = state_name
                return data
        data = {'state': None}
        return data
    else:
        return 'Please Provide Valid Input'
    
# print(validate_state("Sind"))


def list_states(country_name= None):
    response_data = []
    if country_name is not None:
        for country in country_data:
            if country["name"] == country_name:
                data = country
                id = data['id']
                for state in states:
                    if state["country"] == str(id):
                        response_data.append(state)
                return response_data
        data = {'country': 'Invalid Country'}
        return data
    else:
        return 'Please Provide Valid Input'
    
# print(list_states("Pakistan"))
    