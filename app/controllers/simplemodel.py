import random

import networkx as nx


class SimpleRandomGraph:

    def __init__(self, n, p):
        self.n = n
        self.p = p
        self.graph = self.simple_model()

    def get_nx_graph(self):
        return self.graph

    def simple_model(self):
        G = nx.MultiDiGraph()
        for i in range(self.n):
            G.add_node(i)
        for i in range(self.n):
            for j in range(self.n):
                if random.uniform(0, 1) < self.p:
                    G.add_edge(i, j)
        return G