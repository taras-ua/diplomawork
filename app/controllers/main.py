import json
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
import app.controllers.bollobasriordan as br
import app.controllers.simplemodel as sm
import app.controllers.newmodel as nm


def build_graph_request(form):
    request = '/graph/?'
    model = form.cleaned_data['model']
    request += 'model=' + model
    request += '&nodes={}'.format(form.cleaned_data['nodes'])
    if model == 'bollobas-riordan' or model == 'new-model':
        request += '&subnodes={}'.format(form.cleaned_data['subnodes'])
        request += '&initweight={}'.format(form.cleaned_data['initial_weight'])
    if model == 'new-model':
        request += '&forget={}'.format(form.cleaned_data['forget_coef'])
    elif model == 'erdos-renyi':
        request += '&probability={}'.format(form.cleaned_data['probability'])
    return request


def get_graph(request):
    model = request.GET.get('model')
    nodes = int(request.GET.get('nodes'))
    graph = None
    model_name = ''
    model_data = 'n = ' + str(nodes)
    directed = 1
    subnodes_for_new_model = 0
    if model == 'bollobas-riordan':
        model_name = 'Bollobás–Riordan model'
        subnodes = int(request.GET.get('subnodes'))
        initweight = float(request.GET.get('initweight'))
        model_data += ' | m = ' + str(subnodes) + ' | &alpha; = ' + str(initweight)
        graph = br.BollobasRiordan(nodes, subnodes, initweight).get_nx_graph()
    elif model == 'erdos-renyi':
        model_name = 'Erdős–Rényi model'
        directed = 0
        probability = float(request.GET.get('probability'))
        model_data += ' | p = ' + str(probability)
        graph = sm.SimpleRandomGraph(nodes, probability).get_nx_graph()
    elif model == 'new-model':
        model_name = 'Model of forgetting'
        subnodes = int(request.GET.get('subnodes'))
        subnodes_for_new_model = subnodes
        initweight = float(request.GET.get('initweight'))
        forget = float(request.GET.get('forget'))
        model_data += ' | m = ' + str(subnodes) + ' | &alpha; = ' + str(initweight) + ' | &beta; = ' + str(forget)
        graph = nm.NewModel(nodes, subnodes, initweight, forget).get_nx_graph()
    if graph is not None:
        degrees, fractions = get_fraction_of_nodes_with_degree(graph)
        degree_by_node = get_degrees_list(graph)
        nodes = graph.number_of_nodes()
        if model == 'new-model':
            dead_nodes = 0
            for node in graph.nodes():
                if graph.degree(node) == 0:
                    dead_nodes += 1
            nodes -= dead_nodes
        matrix = nx.to_numpy_matrix(graph)
        np.set_printoptions(suppress=True, precision=5)
        matrix_string = ''
        for i in range(len(matrix)):
            matrix_string += str(matrix[i, :]).replace('[', '').replace(']', '').replace('\n ', '') + '\n'
        return json_graph.node_link_data(graph), degrees, fractions, degree_by_node, matrix_string, model_name, model_data, directed, \
               get_diam(graph, model), nodes, graph.number_of_edges(), subnodes_for_new_model


def get_degrees_list(graph):
    degrees = []
    for node in range(graph.number_of_nodes()):
        degrees += [graph.degree(node)]
    return degrees


def get_diam(graph, model):
    diam_check_graph = graph.to_undirected()
    if model == 'new-model':
        for node in diam_check_graph.nodes():
            if diam_check_graph.degree(node) == 0:
                diam_check_graph.remove_node(node)
    try:
        diam = nx.diameter(diam_check_graph)
    except nx.NetworkXError:
        diam = '&infin;'
    finally:
        return diam

def get_fraction_of_nodes_with_degree(graph: nx.MultiDiGraph):
    degrees = {}
    for node in graph.nodes():
        current_degree = graph.degree(node)
        if current_degree > 0:
            if current_degree in degrees.keys():
                temp = degrees.get(current_degree)
                temp += [node]
            else:
                degrees.update({current_degree: [node]})
    fractions = []
    for d_value in sorted(degrees.keys()):
        fractions += [len(degrees.get(d_value)) / graph.number_of_nodes()]
    return sorted(degrees.keys()), fractions