import json
import requests

def question(password, discussion_id, query, question_id=None):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id, 'question_id': question_id}))
    # response = requests.post('http://127.0.0.1:5000/question/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)

def simulate(password, discussion_id, query, question_id=None):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/simulate/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id, 'question_id': question_id}))
    # response = requests.post('http://127.0.0.1:5000/question/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)

def get_discussion_info(password, discussion_id):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/get_discussion_info/' + password, json=json.dumps({'discussion_id': discussion_id}))
    # response = requests.post('http://127.0.0.1:5000/get_discussion_info/' + password, json=json.dumps({'discussion_id': discussion_id}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def dig_deeper(password, discussion_id, question_id, node):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/dig_deeper/' + password, json=json.dumps({'discussion_id': discussion_id, 'question_id': question_id, 'node': node}))
    # response = requests.post('http://127.0.0.1:5000/question/' + password, json=json.dumps({'query':query, 'discussion_id': discussion_id}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
