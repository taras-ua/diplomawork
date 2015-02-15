import json

import networkx as nx
from networkx.readwrite import json_graph
from numpy import linalg as la

import app.controllers.bollobasriordan as br


def build_request(form):
    request = '/graph/?'
    model = form.cleaned_data['model']
    request += 'model=' + model
    request += '&nodes={}'.format(form.cleaned_data['nodes'])
    if model == 'bollobas-riordan':
        request += '&subnodes={}'.format(form.cleaned_data['subnodes'])
    return request


def d3_bollobas_riordan(n, m):
    graph = br.BollobasRiordan(n, m).get_nx_graph()
    json_object = json_graph.node_link_data(graph)
    return json.dumps(json_object)


def get_graph(request):
    model = request.GET.get('model')
    nodes = int(request.GET.get('nodes'))
    if model == 'bollobas-riordan':
        subnodes = int(request.GET.get('subnodes'))
        return d3_bollobas_riordan(nodes, subnodes)


def eigenvalues(graph):
    matrix = nx.to_numpy_matrix(graph)
    print("A = ")
    print(matrix)
    print("Eig A = ")
    print(la.eig(matrix))