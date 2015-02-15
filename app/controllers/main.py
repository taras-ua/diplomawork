import networkx as nx
from networkx.readwrite import json_graph
import numpy as np
from numpy import linalg as la

import app.controllers.bollobasriordan as br
import app.controllers.simplemodel as sm


def build_request(form):
    request = '/graph/?'
    model = form.cleaned_data['model']
    request += 'model=' + model
    request += '&nodes={}'.format(form.cleaned_data['nodes'])
    if model == 'bollobas-riordan':
        request += '&subnodes={}'.format(form.cleaned_data['subnodes'])
    elif model == 'simple':
        request += '&probability={}'.format(form.cleaned_data['probability'])
    return request


def get_graph(request):
    model = request.GET.get('model')
    nodes = int(request.GET.get('nodes'))
    graph = None
    if model == 'bollobas-riordan':
        subnodes = int(request.GET.get('subnodes'))
        graph = br.BollobasRiordan(nodes, subnodes).get_nx_graph()
    elif model == 'simple':
        probability = float(request.GET.get('probability'))
        graph = sm.SimpleRandomGraph(nodes, probability).get_nx_graph()
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
        return json_graph.node_link_data(graph), matrix_string, eigenstring