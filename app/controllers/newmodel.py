import random
import networkx as nx


class NewModel:

    def __init__(self, n, m, a, b):
        self.groups = {}
        self.n = n
        self.m = m
        self.a = a
        self.b = b
        self.graph = self.new_model()

    def get_nx_graph(self):
        return self.graph

    def new_model_step1(self, n, m, a, b):
        G = nx.MultiDiGraph()
        dead_nodes = set()
        weak_nodes = set()
        for i in range(n):
            for j in range(m):
                v = i * m + j
                self.groups[v] = i
                G.add_node(v)
                for twice in range(2):
                    probability = random.uniform(0, 1)
                    prob_sum = (a + G.degree(v)) / ((a + 1) * G.number_of_nodes() - 1 + 2 * twice)
                    if probability <= prob_sum or G.number_of_nodes() == 1:
                        G.add_edge(v, v)
                    else:
                        for node in range(G.number_of_nodes()):
                            if node not in dead_nodes:
                                prob_sum += (G.degree(node) + a - 1) / ((a + 1) * G.number_of_nodes() - 1 + 2 * twice)
                                if probability <= prob_sum:
                                    G.add_edge(v, node)
                                    if node in weak_nodes:
                                        weak_nodes.remove(node)
                                    break
                delete_probability = random.uniform(0, 1)
                delete_prob_sum = 0
                marked_for_delete = -1
                delete_norming_coef = ((1 + b) ** G.number_of_nodes() - 1) / b  # number_of_nodes is actually n+1
                for dead in dead_nodes.union(weak_nodes):
                    delete_norming_coef -= (1 + b) ** (G.number_of_nodes() - (dead + 1))  # number_of_nodes is actually n+1
                for delete_node in range(G.number_of_nodes()):
                    if delete_node not in dead_nodes.union(weak_nodes):
                        delete_prob_sum += (1 + b) ** (G.number_of_nodes() - (delete_node + 1)) / delete_norming_coef # number_of_nodes is actually n+1
                        if delete_probability <= delete_prob_sum:
                            marked_for_delete = delete_node
                            break
                deleted = False
                for delete_connection in range(marked_for_delete + 1, G.number_of_nodes()):
                    if G.has_edge(delete_connection, marked_for_delete):
                        G.remove_edge(delete_connection, marked_for_delete)
                        deleted = True
                        if G.degree(delete_connection) == 0:
                            dead_nodes.add(delete_connection)
                        break
                if not deleted:
                    for delete_connection in range(0, G.number_of_nodes()):
                        if G.has_edge(v, delete_connection):
                            G.remove_edge(v, delete_connection)
                            if G.degree(delete_connection) == 0:
                                dead_nodes.add(delete_connection)
                            break
                if G.degree(marked_for_delete) == 0:
                    dead_nodes.add(marked_for_delete)
        return G

    def new_model_step2(self, G, n):
        G2 = nx.MultiDiGraph()
        for node_num in range(n):
            G2.add_node(node_num)
        for edge in G.edges():
            G2.add_edge(self.groups[edge[0]], self.groups[edge[1]])
        for node in range(G2.number_of_nodes()):
            if G2.degree(node) == G2.number_of_edges(node, node) * 2:
                while G2.degree(node) > 0:
                    G2.remove_edge(node, node)
        return G2

    def new_model(self):
        step1 = self.new_model_step1(self.n, self.m, self.a, self.b)
        return self.new_model_step2(step1, self.n)