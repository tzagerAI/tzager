import json
import requests

def anatomies(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_anatomies/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def diseases(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_diseases/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def symptoms(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_symptoms/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def organisms(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_organisms/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def therapies(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_therapies/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def phenomena(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_phenomena/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def genes(password, concepts_list, pmids=[], filters=[]):
    response = requests.post('https://intoolab.ai/get_genes/' + password, json=json.dumps({'concepts_list':concepts_list, 'pmids': pmids, 'filters': filters}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data