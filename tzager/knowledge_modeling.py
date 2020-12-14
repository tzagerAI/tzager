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

def fill_paths(password, paths):
    response = requests.post('https://cloud.bolooba.com:25556/fill_fractals/' + password , json=json.dumps(paths))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


question = '''
Acute bronchitis is a disease characterized by inflammation of the large airways within the lung accompanied by a cough lasting from 1 to 3 weeks. The inflammation occurs as a result of an airway infection or environmental trigger, with viral infections accounting for an estimated 89% to 95% of cases. Symptomatic treatment of cough is primarily required for patients, though in most cases the condition is self-limiting. Therapy consists of both nonpharmacological and pharmacological options to include antibiotics and antivirals, antitussive agents, protussive agents, and beta-2-agonists. This article reviews the treatment options for acute bronchitis and recommends criteria for use.
'''

paths = get_paths('$biomedicine$', question)
scenarios = paths['scenarios']
for i, s in enumerate(scenarios):
    print('Scenario', i, ':', s, '\n')
path_data = paths['categories']
papers = get_literature('$biomedicine$', path_data, num_papers=10)
# print(papers)
for p_id in papers:
    print('Pmid', p_id, '--- URL:', papers[p_id], '\n')
    
# # papers = knowledge_modeling.get_literature('$biomedicine$', paths['categories'], num_papers=50)
# # print(papers)

# filled_paths = fill_paths('$biomedicine$', paths)
# for s in filled_paths['scenarios']:
#     print(s)
#     print()