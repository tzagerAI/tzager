import json
import requests

def get_path(password, data, type_of_data):
    if type_of_data == 'list':
        data = '|'.join(data)
    
    response = requests.get('https://cloud.bolooba.com:25556/general_goal/' + password + '/' + data + '/' + type_of_data)
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data