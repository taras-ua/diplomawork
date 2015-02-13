import random

import networkx as nx


class BollobasRiordan:

    def __init__(self, n, m):
        self.groups = {}
        self.n = n
        self.m = m
        self.graph = self.bollobas_riordan_model()

    def get_nx_graph(self):
        return self.graph

    def bollobas_riordan_step1(self, n, m):
        G = nx.MultiDiGraph()
        for i in range(n):
            for j in range(m):
                v = i * m + j
                self.groups[v] = i
                G.add_node(v)
                probability = random.uniform(0, 1)
                prob_sum = 1 / (2 * G.number_of_nodes() - 1)
                if probability < prob_sum:
                    G.add_edge(v, v)
                else:
                    for node in range(G.number_of_nodes()):
                        prob_sum += G.degree(node) / (2 * G.number_of_nodes() - 1)
                        if probability < prob_sum:
                            G.add_edge(v, node)
                            break
        return G

    def bollobas_riordan_step2(self, G, n, m):
        G2 = nx.MultiDiGraph()
        for i in range(n):
            G2.add_node(i)
            for j in range(m):
                v = i * m + j
                for node in range(n * m):
                    if G.has_edge(v, node):
                        G2.add_edge(i, self.groups[node])
        return G2

    def bollobas_riordan_model(self):
        step1 = self.bollobas_riordan_step1(self.n, self.m)
        return self.bollobas_riordan_step2(step1, self.n, self.m)