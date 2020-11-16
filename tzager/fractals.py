import json
import requests

def get_data(password, concept):
    
    response = requests.get('https://cloud.bolooba.com:25556/get_fractals/' + password + '/' + concept)
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
