import requests
import json
from collections import Counter

def build_network(data, variables='None'):
    number_of_samples = len(data)
    network = {}
    if variables == 'None':
        for id in data:
            connections = []
            for c in data[id]:
                value = data[id][c]
                connections.append(c + "|" + str(value))
            for var in connections:
                try:
                    network[var] += connections
                except KeyError:
                    network[var] = []
                    network[var] += connections
    else:
        for id in data:
            connections = []
            for c in data[id]:
                if c in variables:
                    value = data[id][c]
                    connections.append(c + "|" + str(value))
            for var in connections:
                try:
                    network[var] += connections
                except KeyError:
                    network[var] = []
                    network[var] += connections
    
    for var in network:
        frequencies = Counter(network[var])
        frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
        network[var] = frequencies
    
    for var in network:
        for conn in network[var]:
            network[var][conn] = round(network[var][conn] / number_of_samples, 3)
    return network


def single_inference(network, q):
    query_variable = q['query_variable'] 
    evidence_variable = q['evidence_variables']
    total_pr = 1

    try:
        if not evidence_variable:
            total_pr *= network[query_variable][query_variable]
        else:
            total_pr *= (network[query_variable][evidence_variable])/network[evidence_variable][evidence_variable]
    except KeyError:
        total_pr = 0

    return total_pr

