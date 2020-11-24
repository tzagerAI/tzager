import networkx as nx
import matplotlib.pyplot as plt
import pickle


def load_example_networks(name='bayesian_network_sm1', save_network_image=False):
    network = pickle.load(open('../data/'+name, 'rb'))
    if save_network_image:
        G = network['graph']
        nx.draw_networkx(G)
        plt.savefig('Bayesian_Network.png')
    return network


def create_network(variable_connections, probabilities, save_network_image=False):    
    G = nx.DiGraph()
    edges = []
    for node in variable_connections:
        for connected_node in variable_connections[node]:
            edges.append((node, connected_node))
    G.add_edges_from(edges)

    if not nx.is_directed_acyclic_graph(G):
        print("Invalid Network ...\n", "Give a directed acyclic graph (DAG) ...")
        return ''
    else:
        nodes = G.nodes()
        is_valid = validate_probability_table(G, nodes, probabilities)

        if save_network_image:
            nx.draw_networkx(G)
            plt.savefig('Bayesian_Network.png')

        if is_valid:
            return {'graph': G, 'probabilities': probabilities}
        else:
            return ''


def validate_probability_table(G, nodes, probabilities_table):
    errors = []
    for node in probabilities_table:
        sum_pr = 0
        if type(probabilities_table[node]) is list:
            for case in probabilities_table[node]:
                value = case[1]
                sum_pr += value
            if sum_pr != 1:
                errors.append('Error in probability distribution of variable: ' + node)
        else:
            sum_pr = 0
            for value in probabilities_table[node]:
                sum_pr += probabilities_table[node][value]
            if sum_pr != 1:
                errors.append('Error in probability distribution of variable: ' + node)
    if not errors:
        return True
    else:
        for er in errors:
            print(er)
        return False

def full_joint_probability(assignment, network):
    assignment_pr = 1
    G = network['graph']
    CPT = network['probabilities']
    nodes = G.nodes
    for n in nodes:
        parents = list(G.predecessors(n))
        if type(CPT[n]) is list:
            case_of_assignment = {}
            for p in parents:
                case_of_assignment[p] = assignment[p]
            for case in CPT[n]:
                if case[0] == case_of_assignment:
                    if assignment[n] == 'T':
                        assignment_pr *= case[1]
                    else:
                        assignment_pr *= (1 - case[1])
                    break
        else:
            assignment_pr *= CPT[n][assignment[n]]
    return {'Pr': assignment_pr}

def inference(query, network, algorithm='enumeration'):
    from itertools import product
    possible_values = ["T", "F"]
    G = network['graph']
    nodes = G.nodes
    query_variables = query['variable']
    evidence_variables = query['given']
    total_probability = 0
    if algorithm == 'enumeration':
        hidden_variables = []
        for n in nodes:
            if n not in query_variables and n not in evidence_variables:
                hidden_variables.append(n)
        print('Query Variables:', list(query_variables.keys()))
        print('Evidence Variables:', list(evidence_variables.keys()))
        print('Hidden Variables:', hidden_variables)
        print()
    
    hidden_variables_dict = {}
    for i,h in enumerate(hidden_variables):
        hidden_variables_dict[i] = h

    assignment = {**query_variables, **evidence_variables}
    
    hidden_variables_possible_assignments = list(product(possible_values, repeat=len(hidden_variables)))
    for pair in hidden_variables_possible_assignments:
        for i, value in enumerate(pair):
            assignment[hidden_variables_dict[i]] = value
        total_probability += full_joint_probability(assignment, network)['Pr']
    return {'Inference Pr': total_probability}



