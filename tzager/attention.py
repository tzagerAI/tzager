import requests
import json


def get_data(password, question, focused_concepts, data_to_get):

    data_dict = {'question': question, 'focused_concepts': focused_concepts, 'data_to_get': data_to_get}
    response = requests.get('https://cloud.bolooba.com:25556/attention/' + password, json=json.dumps(data_dict))
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

