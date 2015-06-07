import random
import networkx as nx


class BollobasRiordan:

    def __init__(self, n, m, a):
        self.groups = {}
        self.n = n
        self.m = m
        self.a = a
        self.graph = self.bollobas_riordan_model()

    def get_nx_graph(self):
        return self.graph

    def bollobas_riordan_step1(self, n, m, a):
        G = nx.MultiDiGraph()
        for i in range(n):
            for j in range(m):
                v = i * m + j
                self.groups[v] = i
                G.add_node(v)
                probability = random.uniform(0, 1)
                prob_sum = a / ((a + 1) * G.number_of_nodes() - 1)
                if probability <= prob_sum or G.number_of_nodes() == 1:
                    G.add_edge(v, v)
                else:
                    for node in range(G.number_of_nodes()):
                        prob_sum += (G.degree(node) + a - 1) / ((a + 1) * G.number_of_nodes() - 1)
                        if probability <= prob_sum:
                            G.add_edge(v, node)
                            break
        return G

    def bollobas_riordan_step2(self, G, n):
        G2 = nx.MultiDiGraph()
        for node_num in range(n):
            G2.add_node(node_num)
        for edge in G.edges():
            G2.add_edge(self.groups[edge[0]], self.groups[edge[1]])
        return G2

    def bollobas_riordan_model(self):
        step1 = self.bollobas_riordan_step1(self.n, self.m, self.a)
        return self.bollobas_riordan_step2(step1, self.n)