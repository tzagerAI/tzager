from tqdm import tqdm
from collections import Counter


def values_for_variables(data):
    all_possible_variables = {}

    for id in data:
        for variable in data[id]:
            value = data[id][variable]
            try:
                all_possible_variables[variable].append(str(value))
            except KeyError:
                all_possible_variables[variable] = []
                all_possible_variables[variable].append(str(value))

    for variable in all_possible_variables:
        all_possible_variables[variable] = list(set(all_possible_variables[variable]))
    return all_possible_variables


def conditional_prob(data, q):
    number_of_samples = len(data)
    variables_join = {}
    query_variable = q['query_variable']['variable'] + '===' + str(q['query_variable']['value'])
    evidence_variable = [x['variable'] + '===' + str(x['value']) for x in q['evidence_variables']]
    for id in data:
        instance = []
        for variable in data[id]:
            value = data[id][variable]
            instance.append(variable + '===' + str(value))
        variables_join[id] = instance

    if not evidence_variable:
        query_hits = 0
        for id in variables_join:
            if query_variable in variables_join[id]:
                query_hits += 1
        total_pr = round(query_hits/number_of_samples, 3)
    else:
        evidence_query_join = 0
        evidence_join = 0
        for id in variables_join:
            if set(evidence_variable) <= set(variables_join[id]):
                evidence_join += 1
            if set(evidence_variable + [query_variable]) <= set(variables_join[id]):
                evidence_query_join += 1
        if evidence_join != 0:
            total_pr = round(evidence_query_join/evidence_join, 3)
        else:
            total_pr = 0
    return total_pr


def prob_event(data, variables, q, topn=5):
    import itertools
    query_variable = q['query_variable']
    evidence_variables = q['evidence_variables']
    data_values = {}
    for ev in evidence_variables:
        data_values[ev] = variables[ev]
    
    cases = [dict(zip(data_values, x)) for x in itertools.product(*data_values.values())]
    scores = []
    with tqdm(total=len(cases)) as pbar:
        for case in cases:
            q_prime = {'query_variable': None, 'evidence_variables': []}
            q_prime['query_variable'] = query_variable
            for v in case:
                q_prime['evidence_variables'].append({'variable':v, 'value': case[v]})
            prob = conditional_prob(data, q_prime)
            pbar.update(1)
            scores.append((q_prime, prob))
    
    scores =  sorted(scores, key=lambda x: x[1], reverse=True)[:topn]
    for s in scores:
        print('For case:', s[0])
        print('Pr:', s[1])
        print()
    return scores


#### PREMIUM ###
def suggest_belief(password, query, topn=10):
    import requests, json
    response = requests.post('https://cloud.bolooba.com:25556/suggest_belief/' + password + '/' + str(topn), json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
        data = sorted(data.items(), key=lambda x: x[1], reverse=True)
        data = dict(data)
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


def compute_prob(password, query):
    import requests, json
    response = requests.post('https://cloud.bolooba.com:25556/tzager_prob/' + password, json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data

def targeted_prob(password, query, a_rate=2, report=False):
    import requests, json
    response = requests.post('https://cloud.bolooba.com:25556/' + password + '/' + str(a_rate), json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
        if report:
            print('================= REPORT =================')
            
            
            print('\n\n----------------------------- Probabilities Data --------------------\n\n')
            print('Probability:', data['step1']['prob'], '\n')
            print('Probability analysis per given variable:')
            for g in data['step1']['prob per given variable']:
                print(g, ':', data['step1']['prob per given variable'][g])
    
            print('\n\n--- Probabilities Analysis For Suggested Beliefs (based on given) ---\n\n')
            temp_data = []
            for b in data['step2']:
                temp_data.append((b, data['step2'][b]['prob'], data['step2'][b]['prob per given variable']))
            temp_data = sorted(temp_data, key=lambda x: x[1], reverse=True)
            for pair in temp_data:
                b = pair[0]
                prob = pair[1]
                per_given_v = pair[2]
                print('Belief:', b)
                print('Probability:', prob)
                print('Probability analysis per given variable:')
                for g in per_given_v:
                    print(g, ':', per_given_v[g])
                print()
            print("\n\n-------------- Missing Given variables to complete Belief ------------\n\n")
            for categ in data['step3']:
                print(categ + ' missing:', [c for c in data['step3'][categ] if c not in query['given_variables']])
                print()
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data
