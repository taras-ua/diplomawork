import json
import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
from numpy import linalg as la
import app.controllers.bollobasriordan as br
import app.controllers.simplemodel as sm
import app.controllers.newmodel as nm
import app.controllers.probabilities as prob


def build_graph_request(form):
    request = '/graph/?'
    model = form.cleaned_data['model']
    request += 'model=' + model
    request += '&nodes={}'.format(form.cleaned_data['nodes'])
    if model == 'bollobas-riordan' or model == 'new-model':
        request += '&subnodes={}'.format(form.cleaned_data['subnodes'])
    elif model == 'simple':
        request += '&probability={}'.format(form.cleaned_data['probability'])
    return request


def build_probabilities_request(form):
    request = '/probabilities/?'
    spec = form.cleaned_data['spec']
    request += 'spec=' + spec
    request += '&edges={}'.format(form.cleaned_data['edges'])
    if spec == 'degree':
        request += '&degree={}'.format(form.cleaned_data['degree'])
    request += '&time={}'.format(form.cleaned_data['time'])
    return request


def get_graph(request):
    model = request.GET.get('model')
    nodes = int(request.GET.get('nodes'))
    graph = None
    model_name = ''
    model_data = 'Nodes: ' + str(nodes)
    if model == 'bollobas-riordan':
        model_name = 'Bollobás–Riordan model'
        subnodes = int(request.GET.get('subnodes'))
        model_data += ' | Subnodes: ' + str(subnodes)
        graph = br.BollobasRiordan(nodes, subnodes).get_nx_graph()
    elif model == 'simple':
        model_name = 'Simple random directed multigraph'
        probability = float(request.GET.get('probability'))
        model_data += ' | Probability: ' + str(probability)
        graph = sm.SimpleRandomGraph(nodes, probability).get_nx_graph()
    elif model == 'new-model':
        model_name = 'New Model'
        subnodes = int(request.GET.get('subnodes'))
        model_data += ' | Subnodes: ' + str(subnodes)
        graph = nm.NewModel(nodes, subnodes).get_nx_graph()
    if graph is not None:
        matrix = nx.to_numpy_matrix(graph)
        np.set_printoptions(suppress=True, precision=5)
        eigenvals, eigenvecs = la.eig(matrix)
        eigenstring = ''
        matrix_string = ''
        eig_num = 0
        for i in range(eigenvals.size):
            val = eigenvals[i]
            matrix_string += str(matrix[i, :]).replace('[', '').replace(']', '') + '<br>'
            if val != 0:
                eig_num += 1
                eigenstring += '<b>&lambda;<sub>' + str(eig_num) + '</sub></b> = ' + str(val) + '; '
                eigenstring += '<b>f<sub>' + str(eig_num) + '</sub></b> = ( '
                eigenstring += str(eigenvecs[:, i]).replace('[', '').replace(']', '')
                eigenstring += ' )<sup>T</sup><br>'
        return json_graph.node_link_data(graph), matrix_string, eigenstring, model_name, model_data


def get_probabilities(request):
    spec = request.GET.get('spec')
    initial_edges_value = int(request.GET.get('edges'))
    time_length = int(request.GET.get('time'))
    x = None
    y = None
    spec_name = ''
    spec_data = 'Initial edges: ' + str(initial_edges_value) + ' | Time period: ' + str(time_length)
    main_init = initial_edges_value
    if spec == 'edges':
        spec_name = 'Total number of edges'
        x, y = prob.edges(initial_edges_value, time_length)
    if spec == 'degree':
        initial_degree_value = int(request.GET.get('degree'))
        main_init = initial_degree_value
        spec_name = 'Degree of single node'
        spec_data = 'Initial degree: ' + str(initial_degree_value) + ' | ' + spec_data
        x, y = prob.degree(initial_edges_value, initial_degree_value, time_length)
    if x is not None and y is not None:
        return spec_name, spec_data, json.dumps(x.tolist()), json.dumps(y.tolist()), main_init