import json

import networkx as nx
from networkx.readwrite import json_graph
from numpy import linalg as la

import app.controllers.bollobasriordan as br


def d3_bollobas_riordan(n, m):
    graph = br.BollobasRiordan(n, m).get_nx_graph()
    json_object = json_graph.node_link_data(graph)
    return json.dumps(json_object)


def eigenvalues(graph):
    matrix = nx.to_numpy_matrix(graph)
    print("A = ")
    print(matrix)
    print("Eig A = ")
    print(la.eig(matrix))