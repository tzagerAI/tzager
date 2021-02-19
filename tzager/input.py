import json
import requests

def abstract_scopes(password, abstracts):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/abstract_scopes/' + password, json=json.dumps({'abstracts': abstracts}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
    