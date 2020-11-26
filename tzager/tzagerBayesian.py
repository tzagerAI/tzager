import requests
import json
from collections import Counter


def values_for_variables(data):
    all_possible_variables = []

    for id in data:
        for variable in data[id]:
            value = data[id][variable]
            all_possible_variables.append(variable + '=' + str(value))
    
    all_possible_variables = list(set(all_possible_variables))
    return all_possible_variables


def conditional_prob(data, q):
    number_of_samples = len(data)
    variables_join = {}
    query_variable = q['query_variable'] 
    evidence_variable = q['evidence_variables']
    if evidence_variable:
        print('Calculating:', "Pr[" + query_variable + ' | ' + ','.join(evidence_variable) + ']')
    else:
        print('Calculating:', "Pr[" + query_variable + ']')
    all_possible_variables = []

    for id in data:
        instance = []
        for variable in data[id]:
            value = data[id][variable]
            instance.append(variable + '=' + str(value))
            all_possible_variables.append(variable + '=' + str(value))
        variables_join[id] = instance
    
    all_possible_variables = list(set(all_possible_variables))

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
