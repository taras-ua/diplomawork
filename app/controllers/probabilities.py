from copy import copy
from matplotlib import pyplot
import numpy as np


def recursive_sets_builder(bound, array_current, array_result):
    array_result += [copy(array_current)]
    i = len(array_current)
    exit_point = True
    while i > 0:
        i -= 1
        if array_current[i] != bound:
            array_current[i] += 1
            exit_point = False
            break
    if not exit_point:
        array_result = recursive_sets_builder(bound, array_current, array_result)
    return array_result


def markov_probabilities(m, t, k):
    s = np.zeros(t - k)
    s.fill(m)
    subset = []
    subset = recursive_sets_builder(m + k, s, subset)
    summed = 0
    for A in subset:
        multiplied = 1
        for x in A:
            multiplied *= 1 / (x + 1)
        summed += multiplied
    return summed * m / (m + k)


def main():
    input_m = 1
    input_t = 20
    x_axis = np.arange(0, input_t + 1, 1)
    y_axis = np.zeros(input_t + 1)
    for i in range(input_t + 1):
        y_axis[i] = markov_probabilities(input_m, input_t, x_axis[i])
    pyplot.xlabel('Connections growth, k')
    pyplot.ylabel('Probability, P[t, m, m+k]')
    pyplot.title('Starrting from m = {} during t = {}'.format(input_m, input_t))
    pyplot.plot(x_axis, y_axis)
    sum = 0
    for x in y_axis:
        sum += x
    print(sum)
    pyplot.show()


main()