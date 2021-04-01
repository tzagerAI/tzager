import json
import requests

def question(password, pmids, query):
    response = requests.post('https://intoolab.ai/paper_filtered_question/' + password, json=json.dumps({'query':query, 'pmids': pmids}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data