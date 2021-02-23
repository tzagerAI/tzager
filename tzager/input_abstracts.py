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


def complemetary_abstracts(password, data_for_complemetary_abstracts):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/complemetary_abstracts/' + password, json=json.dumps({'data_for_complemetary_abstracts': data_for_complemetary_abstracts}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def scientific_analysis(password, abstracts, data_for_scientific_analysis, complemetary_data):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/scientific_analysis_abstracts/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'abstracts': abstracts, 'complemetary_data': complemetary_data}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


def abstract_augment_nodes(password, abstracts, data_for_scientific_analysis, complemetary_data, scopes):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/abstract_augment_nodes/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'abstracts': abstracts, 'complemetary_data': complemetary_data, 'scopes': scopes}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def abstract_augment_scopes(password, abstracts, data_for_scientific_analysis, complemetary_data, scopes):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/abstract_augment_scopes/' + password, json=json.dumps({'data_for_scientific_analysis': data_for_scientific_analysis, 'abstracts': abstracts, 'complemetary_data': complemetary_data, 'scopes': scopes}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def question_hbn(password, question):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question_hbn/' + password, json=json.dumps({'question_text': question}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def question_abstracts(password, question, abstracts):
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/question_abstracts/' + password, json=json.dumps({'question_text': question, 'abstracts': abstracts}))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data