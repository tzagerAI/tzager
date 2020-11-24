import json
import requests

def get_data(password, concepts_list):
    concepts_list = '|'.join(concepts_list)
    response = requests.get('https://cloud.bolooba.com:25556/get_fractals/' + password + '/' + concepts_list)
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
