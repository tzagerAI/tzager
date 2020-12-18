import json
import requests

def get_data(password, new_concept, based_on, data_to_get):

    data_dict = {'new_concept': new_concept, 'based_on': based_on, 'data_to_get': data_to_get}
    response = requests.get('https://cloud.bolooba.com:25556/train/' + password, json=json.dumps(data_dict))
    if response.status_code == 200:
        data = dict(response.json())        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

