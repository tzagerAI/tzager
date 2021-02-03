import json
import requests

def question(password, discussion_id, query):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    