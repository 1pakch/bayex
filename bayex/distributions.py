"""Marginal and conditional distributions with finite support

Conditional distributions are represented by callables which return a marginal
distribution when called with conditioning variables as arguments.

Marginal distributions are represented by dicts where keys are the possible
values and the dicts' values are respective probabilities. Marginal
distributions are also callable with no arguments as they are also
conditional distributions with empty conditioning set.
"""

import collections


class Marginal(dict):

    def __call__(self):
        'Marginal is conditional distribution with empty conditioning set'
        return self

    def __str__(self):
        'As a dict prefixed by "m"'
        return 'm' + dict.__str__(self)

    def __repr__(self):
        'As a dict prefixed by "m"'
        return 'm' + dict.__repr__(self)

    @staticmethod
    def from_mixture(items):
        'Construct by summing dists in (p, dist) with weights p'
        result = collections.defaultdict(lambda: 0)
        for dist, p_dist in items:
            for value, p_value in dist.items():
                result[value] += p_value * p_dist
        return Marginal(result)



class Constant(Marginal):

    def __init__(self, value):
        'A marginal distribution taking a single value with probability 1'
        Marginal.__init__(self, {value: 1})


class Bernoulli(Marginal):

    def __init__(self, p, values=(0, 1)):
        'A marginal distribution taking values[1] with probability p'
        probs = (1 - p, p)
        vpdict = {v: p for p, v in zip(probs, values)}
        Marginal.__init__(self, vpdict)


class Uniform(Marginal):

    def __init__(self, values):
        'A marginal distribution taking values with equal probabilities'
        values = list(values)
        n = len(values)
        probs = [1 / n] * n
        vpdict = {v: p for p, v in zip(probs, values)}
        Marginal.__init__(self, vpdict)

