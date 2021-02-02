from collections import Counter

def suggest_beliefs(password, query):
    import requests, json
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/suggest_beliefs/' + password, json=json.dumps(query))
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
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/hbn_compute_prob/' + password, json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


def branch_conditions(password, query):
    import requests, json
    response = requests.post('http://tzagerlib1-env.eba-wjp8tqpj.eu-west-2.elasticbeanstalk.com/branch_conditions/' + password, json=json.dumps(query))
    if response.status_code == 200:
        data = dict(response.json())
    else:
        data = {'error': response.status_code}
        data = dict(data)
    return data


def targeted_prob(password, query, a_rate=2, report=False):
    import requests, json
    response = requests.post('https://cloud.bolooba.com:25556/targeted_prob/' + password + '/' + str(a_rate), json=json.dumps(query))
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


