import json
import math
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


from opensimplex import OpenSimplex




def all_random(x, y):
    return random.random() * 20.0


def simple_sine(x, y):
    return math.sin(x) * 5.0 + math.sin(y) * 5.0


def multiple_octaves(octaves, start_amplitude):
    parameters = []
    for i in range(octaves):
        parameters.append({
            'offset': random.random() * 2 * math.pi,
            'frequency': 2**i,
            'amplitude': start_amplitude / float(i+1),
        })

    def noise(x, y):
        value = 0
        for p in parameters:
            x_part = math.sin(
                (x / float(WIDTH))
                * p['frequency']
                * 2 * math.pi
                + p['offset']
            )
            y_part = math.sin(
                (y / float(HEIGHT))
                * p['frequency']
                * 2 * math.pi
                + (x_part % (2 * math.pi))
            )
            value += y_part * p['amplitude']

        return value

    return noise


power_simplex = OpenSimplex(int(random.random() * 100))


def power(exponent):
    def noise(x, y):
        value = (power_simplex.noise2d(x/3.0, y/3.0) + 1.0) / 2.0

        return (value ** exponent) * 20.0

    return noise


def simplex():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        return (tmp.noise2d(x/3.0, y/3.0) + 1) * 10.0

    return noise


def simple_curve(value):
    start = 0.4
    end = 0.6
    if value < start:
        return 0.0
    if value > end:
        return 1.0
    return (value - start) * (1 / (end - start))


def interpolate(a, b, weight):
    new_weight = simple_curve(weight)

    return a * (1 - new_weight) + b * new_weight


def simple_scurve():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        noise = (tmp.noise2d(x/5.0, y/5.0) + 1) / 2.0

        return interpolate(0.0, 1.0, noise) * 10.0

    return noise


def plains():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x / noisyness, y / noisyness) + 1)

        value = value**0.25

        value = value - 0.6

        if value < 0:
            value = 0

        return value * HEIGHT * 2

    return noise


def mountains():
    tmp = OpenSimplex(int(random.random() * 10000))

    def noise(x, y):
        value = (tmp.noise2d(x / noisyness, y / noisyness) + 1)

        value = value

        return value * HEIGHT * 0.57

    return noise


def combined():
    m_values = mountains()
    p_values = plains()
    # weights = simple_scurve()
    weights = multiple_octaves(1, 1)

    def noise(x, y):
        m = m_values(x, y) / 20
        p = p_values(x, y)
        w = weights(x, y) / 3

        return (p * w) + (m * (1 - w)) * 20

    return noise


def generate(value):
    values = []

    for x in range(WIDTH):
        for y in range(WIDTH):
            values.append([x, y, value(x, y)])

    # return values
    return pd.DataFrame(values, columns=list('xyz'))

WIDTH = 100
HEIGHT = 100
tmp = OpenSimplex()
noisyness = 22.0 #lower is noisier
file_name = 'hillclimber.csv'

if __name__ == '__main__':
    # You can try one of these
    # data = generate(plains())
    # data = generate(mountains())
    # data = generate(multiple_octaves(1, 1))

    data = generate(combined())
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_trisurf(data['x'], data['y'], data['z'], cmap=cm.coolwarm, linewidth=0, antialiased=False)
    plt.show()
    data.to_csv(file_name, index=False)