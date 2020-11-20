import networkx as nx
import matplotlib.pyplot as plt
import pickle


def load_example_networks(name='bayesian_network_sm1', save_network_image=False):
    network = pickle.load(open('data/'+name, 'rb'))
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
    invalid_nodes = []
    for node in nodes:
        parents = list(G.predecessors(node))
        if not parents:
            if not (node in probabilities_table and type(probabilities_table[node]) == float): 
                invalid_nodes.append('No probability for ' + node + ' in probabilities data.')
        else:
            for p in parents:
                if p not in list(probabilities_table[node].keys()):
                    invalid_nodes.append('Missing probability for ' + node + '|' + p + '.')
    if not invalid_nodes:
        return True
    else:
        for error in invalid_nodes:
            print(error)
        return False

