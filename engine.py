from pomegranate import *
import json
import sys

def process_input(data):
    """Processes the input data to generate a list of discrete distributions for the parent nodes, as well as additional lists and dictionaries that will be useful later

    Parameters
    ----------
    data : list
        A list of dictionaries corresponding to the probabilities associated with each node. Also includes values for beliefs and query

    Returns
    -------
    distributions
        A dictionary of JSON objects containing discrete distributions for parent nodes
    tables_data
        A list of tables that will require further processing before generating conditional probability tables for non-parent nodes
    beliefs
        A dictionary containing beliefs as declared in the input file
    query
        A list containing the query as declared in the input file
    edges
        A list of tuples corresponding to the Bayesian network structure as described in the input file 
    """
    distributions = {}
    beliefs = {}
    query = []
    edges = []
    tables_data = []
    pos_temp = []
    neg_temp = []
    for node in data:
        table = []
        pos = []
        neg = []
        for key in node.keys():
            if key == 'BELIEF':
                append = 0
                new_key = node.get(key).replace('-', '')
                beliefs[new_key] = node.get(key)
            elif key == 'QUERY':
                append = 0
                query.append(node.get(key))
            else:
                if key.find('|') == -1:
                    append = 0
                    distributions[key] = DiscreteDistribution({key: node.get(key), '-' + key: 1 - node.get(key)})
                else:
                    append = 1
                    info = key.split('|')
                    if info[1].find('-') == -1:
                        for i in range(len(info[1])):
                            edges.append((info[1][i], info[0]))
                    pos_row = []
                    neg_row = []
                    flag = 0
                    for i in range(len(info[1])):
                        if flag == 1:
                            flag = 0
                            continue
                        elif info[1][i] == '-':
                            pos_row.append(info[1][i]+ info[1][i + 1])
                            neg_row.append(info[1][i]+ info[1][i + 1])
                            flag = 1
                        else:
                            pos_row.append(info[1][i])
                            neg_row.append(info[1][i])
                    pos_row.append(info[0])
                    pos_row.append(node.get(key))
                    pos_temp = pos_row
                    neg_row.append('-' + info[0])
                    neg_row.append(1 - node.get(key))
                    neg_temp = neg_row
                if append == 1:
                    pos.append(pos_temp)
                    neg.append(neg_temp)
        table = pos + neg
        if append == 1:
            tables_data.append(table)
    return distributions, tables_data, beliefs, query, edges

def get_child_parents(edges):
    """Puts each non-parent node together with its parents

    Parameters
    ----------
    edges : list
        A list of tuples corresponding to the Bayesian network structure as described in the input file 

    Returns
    -------
    child_parents
        A dictionary with non-parent nodes as keys and their parents as values
    """
    child_parents = {}
    for e in edges:
        if e[1] in child_parents.keys():
            child_parents[e[1]].append(e[0])
        else:
            child_parents[e[1]] = [e[0]]
    return child_parents

def update_distributions(distributions, tables_data, child_parents):
    """Generates conditional probability tables from the tables_data list and adds them to the distributions dictionary

    Parameters
    ----------
    distributions : dict
        A dictionary of JSON objects containing discrete distributions for parent nodes 
    tables_data : list
        A list of tables that will require further processing before generating conditional probability tables for non-parent nodes
    child_parents : dict
        A dictionary with non-parent nodes as keys and their parents as values
    """
    conditional = {}
    for t in tables_data:
        if t[0][-2] in child_parents.keys():
            parents_table = []
            parents_list = child_parents[t[0][-2]]
            for p in parents_list:
                parents_table.append(distributions[p])
            conditional[t[0][-2]] = ConditionalProbabilityTable(t, parents_table)
            distributions.update(conditional)

def generate_states(distributions):
    """Generates valid Bayesian network states

    Parameters
    ----------
    distributions : dict
        A dictionary of JSON objects containing discrete distributions for both parent and non-parent nodes

    Returns
    -------
    states
        A dictionary of JSON objects containing valid Bayesian network states
    """
    states = {}
    for state in distributions:
        states[state] = State(distributions[state], name=state)
    return states

def create_bayesian_network(states, edges):
    """Creates a Bayesian network given valid states and edges 

    Parameters
    ----------
    states : dict
        A dictionary of JSON objects containing valid Bayesian network states
    edges : dict
        A list of tuples corresponding to the Bayesian network structure as described in the input file 

    Returns
    -------
    network
        A JSON object corresponding to the final Bayesian network
    """
    network = BayesianNetwork()
    for s in states:
        network.add_state(states[s])
    for e in edges:
        network.add_edge(states[e[0]], states[e[1]])
    return network

def process_output(network, predictions, beliefs, query):
    """Processes the final predictions prior to writing them to a file

    Parameters
    ----------
    network : dict
        A JSON object corresponding to the final Bayesian network
    predictions : dict
        A JSON object corresponding to the predicted probabilites for each node given beliefs and a query
    beliefs : dict
        A dictionary containing beliefs as declared in the input file
    query : list
        A list containing the query as declared in the input file

    Returns
    -------
    output_query
        A string for the name of the output file
    output_json
        A JSON object containing the final predictions
    """
    output_query = ''
    output_probability = ''
    for state, prediction in zip(network.states, predictions):
        original_query = query[0]
        q = query[0].replace('-', '')
        if q == state.name:
            output_predictions = ''
            for key in beliefs.keys():
                output_predictions += beliefs[key]
            output_query = original_query + '|' + output_predictions
            output_probability = prediction.parameters[0]
    output_json = json.dumps(output_probability)
    return output_query, output_json

def main(path):
    """Predicts the probability of the query as declared in the input file and writes it to an output file

    Parameters
    ----------
    path : str
        A string corresponding to the relative path to the input file
    """
    with open(path, 'r') as f:
        data = json.load(f)

    distributions, tables_data, beliefs, query, edges = process_input(data)
    child_parents = get_child_parents(edges)
    update_distributions(distributions, tables_data, child_parents)

    states = generate_states(distributions)

    network = create_bayesian_network(states, edges)
    network.bake()

    predictions = network.predict_proba(beliefs)

    output_query, output_json = process_output(network, predictions, beliefs, query)

    with open(output_query + '.json', 'w') as json_file:
        json_file.write(output_json)

    print(f'A new JSON file has been created containing the probability assigned to the query "{output_query}".')

if __name__ == '__main__':
    main(sys.argv[1])