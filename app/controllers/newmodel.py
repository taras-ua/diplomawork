import random

import networkx as nx


class NewModel:

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
                probability_of_delete = random.uniform(0, 1)
                prob_sum_of_delete = 1 / (G.number_of_edges() + 1)
                mark_for_delete = -1
                if not probability_of_delete < prob_sum_of_delete:
                    for node in range(G.number_of_nodes()):
                        if not G.degree(node) == 0:
                            prob_sum_of_delete += 1 / (G.number_of_edges() + 1)
                            if probability_of_delete < prob_sum_of_delete:
                                mark_for_delete = node
                                break
                probability = random.uniform(0, 1)
                if v == 0:
                    G.add_edge(v, v)
                else:
                    prob_sum = 0
                    for node in range(G.number_of_nodes()):
                        prob_sum += G.degree(node) / (2 * G.number_of_edges())
                        if probability < prob_sum:
                            G.add_edge(v, node)
                            break
                if mark_for_delete > -1:
                    for node in range(G.number_of_nodes()):
                        if G.has_edge(mark_for_delete, node):
                            G.remove_edge(mark_for_delete, node)
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