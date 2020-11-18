import json
import requests


def get_data(password, question, type_of, path='None'):
    if type_of == 'list':
        question = '|'.join(question)
    
    response = requests.get('https://cloud.bolooba.com:25556/get_why/' + password + '/' + question + '/' + type_of + '/' + path)
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data