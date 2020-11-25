import requests
import json
from collections import Counter

def build_network(data, variables='None'):
    variables_connections = {}
    if variables == 'None':
        for id in data:
            connections = []
            for c in data[id]:
                value = data[id][c]
                connections.append(c + "|" + str(value))
            for var in connections:
                try:
                    variables_connections[var] += connections
                except KeyError:
                    variables_connections[var] = []
                    variables_connections[var] += connections
    else:
        for id in data:
            connections = []
            for c in data[id]:
                if c in variables:
                    value = data[id][c]
                    connections.append(c + "|" + str(value))
            for var in connections:
                try:
                    variables_connections[var] += connections
                except KeyError:
                    variables_connections[var] = []
                    variables_connections[var] += connections
    
    for var in variables_connections:
        frequencies = Counter(variables_connections[var])
        frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
        variables_connections[var] = frequencies

    return variables_connections

