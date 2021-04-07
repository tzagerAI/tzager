import json
import requests


def get_network(password, pmids):
    response = requests.post('https://intoolab.ai/get_network/' + password, json=json.dumps({'pmids': pmids}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
