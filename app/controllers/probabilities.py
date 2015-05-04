import itertools
import numpy as np


'''Edges count'''


def edge_growth_probability(m, t, k):
    summed = 0
    for A in itertools.combinations_with_replacement(range(m, m + k + 1), t - k):
        multiplied = 1
        for x in A:
            multiplied *= 1 / (x + 1)
        summed += multiplied
    return summed * m / (m + k)


def edges(init, time):
    x_axis = np.arange(0, time + 1, 1)
    y_axis = np.zeros(time + 1)
    for i in range(time + 1):
        y_axis[i] = edge_growth_probability(init, time, x_axis[i])
    return x_axis, y_axis


'''Vertex degree'''


def get_staying_variants(list, word, sum, size):
    if sum == size:
        list += [word]
    elif sum < size:
        get_staying_variants(list, word + 'u', sum + 2, size)  # up
        get_staying_variants(list, word + 's', sum + 1, size)  # stand
        get_staying_variants(list, word + 'd', sum + 2, size)  # down


def vertex_degree_probability(m, d, t, k):  # TODO problem: going down to zero without probability of coming back
    if d + k < 0:
        return 0
    summed = 0
    staying_variants = []
    get_staying_variants(staying_variants, '', 0, t - abs(k))
    for type_of_staying in staying_variants:
        for A in itertools.combinations_with_replacement(range(k + 1) if k > 0 else range(k, 1), len(type_of_staying)):
            multiplied = 1
            for i in range(len(A)):
                x = A[i]
                if d + x > 0:
                    if type_of_staying[i] == 'u':  # we are going up and down to save position during this step
                        multiplied *= (d + x) * (m + 1 - d) / (2 * (m + x) * (m + x + 1))
                        multiplied *= (d + x + 1) * (2 * m - d + x + 1) / (2 * (m + x + 1) * (m + x + 2))
                    elif type_of_staying[i] == 'd':  # we are going down and up to save position during this step
                        multiplied *= (d + x) * (2 * m - d + x) / (2 * (m + x) * (m + x + 1))
                        multiplied *= (d + x - 1) * (m + 1 - d) / (2 * (m + x - 1) * (m + x))
                    else:  # we are standing on same position during this step
                        multiplied *= ((d + x) ** 2 + (m + 1 - d) * (2 * m - d + x)) / (2 * (m + x) * (m + x + 1))
        summed += multiplied
    koef = 1
    if k != 0:
        if k > 0:
            for step in range(k):
                koef *= (d + step) / (m + step) ** 2
            koef *= ((m + 1 - d) / 2) ** k / (m * (m + k))
        else:
            for step in range(k + 1, 1):
                koef *= (d + step) * (2 * m - d + step) / (m + step) ** 2
            koef *= (m + k + 1) / ((m + 1) * 2 ** k)
    return summed * koef


def degree(init_edges, init_degree, time):
    x_axis = np.arange(-time, time + 1, 1)
    y_axis = np.zeros(2 * time + 1)
    for i in range(2 * time + 1):
        y_axis[i] = vertex_degree_probability(init_edges, init_degree, time, x_axis[i])
    return x_axis, y_axis