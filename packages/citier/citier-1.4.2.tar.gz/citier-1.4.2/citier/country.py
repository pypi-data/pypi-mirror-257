import json
def read_json(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

states = read_json('json/state.json')
country_data = read_json('json/countries.json')

def validate_country(country_name=None):
    if country_name is not None:
        for country in country_data:
            if country["name"] == country_name:
                data = country
                return data
        data = {'country': None}
        return data
    else:
        return 'Please Provide Valid Input'


# print(validate_country())

def countries_list(limit_start=None, limit_end=None):
    data = []
    if limit_start is not None and limit_end is not None:
        if limit_start <= limit_end:
            for country in country_data:
                if country['id'] >= limit_start and country['id'] <= limit_end:
                    data.append(country) 
            return data
        else:
            return 'Invalid Limit'
    else:
        for country in country_data:
            data.append(country) 
        return data
        
# print(countries_list(1,2))
# print(countries_list(2,1))
# print(countries_list())