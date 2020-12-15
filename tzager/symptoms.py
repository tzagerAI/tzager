import json
import requests


def get_data(password, concept_list, filters=[]):
    data_dict = {'concept_list': concept_list, 'filters': filters}
    
    response = requests.get('https://cloud.bolooba.com:25556/symptoms_data/' + password, json=json.dumps(data_dict))
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
