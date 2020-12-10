import requests, json


def get_paths(password, question):
    query = {'question': question}
    response = requests.post('https://cloud.bolooba.com:25556/path_on_input/' + password, json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def get_literature(password, paths, num_papers=50):
    response = requests.post('https://cloud.bolooba.com:25556/literature_hits/' + password + '/' + str(num_papers), json=json.dumps(paths))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def fill_fractals(password, paths, topn=5, report=True):
    response = requests.post('https://cloud.bolooba.com:25556/fill_fractals/' + password + '/' + str(topn), json=json.dumps(paths))
    if response.status_code == 200:
        data = dict(response.json())
        if report:
            print()
            print('BODY PATH')
            for categ in data['Body']:
                print(categ, ':', data['Body'][categ])
            print('\n---------------------------------------------\n')
            print('DISEASE PATH')
            for categ in data['Disease']:
                print(categ, ':', data['Disease'][categ])
            print('\n---------------------------------------------\n')
            print('THERAPY PATH')
            for categ in data['Therapy']:
                print(categ, ':', data['Therapy'][categ])
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


