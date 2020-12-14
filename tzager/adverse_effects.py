import json
import requests


def get_data(password, concept_list, filters='None'):

    data_dict = {'concept_list': concept_list, 'filters': filters}
    response = requests.get('http://127.0.0.1:5000/adverse_effects/' + password, json=json.dumps(data_dict))
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

