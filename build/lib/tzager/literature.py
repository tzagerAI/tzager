import json
import requests


def get_data(password, concept_list, n_papers):
    concept_list = '|'.join(concept_list)
    
    response = requests.get('https://cloud.bolooba.com:25556/literature_data/' + password + '/' + concept_list + '/' + n_papers)
    if response.status_code == 200:
        data = dict(response.json())
        
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
