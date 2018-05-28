'Bayesian network from Wikipedia'

import networkx as nx
from bayex import *

rains = Bernoulli(0.2)

def sprinkler(rains):
    return Bernoulli(0.01) if rains else Bernoulli(0.4)

def grass_wet(sprinkler, rains):
    if not sprinkler and not rains:
        return Constant(0)
    elif not sprinkler and rains:
        return Bernoulli(0.8)
    elif sprinkler and not rains:
        return Bernoulli(0.9)
    else: # sprinkler and rains
        return Bernoulli(0.99)


model = nx.DiGraph()
# Add states
model.add_node('rains', dist=rains)
model.add_node('sprinkler', dist=sprinkler)
model.add_node('grass_wet', dist=grass_wet)
# Connect states
model.add_edge('rains', 'sprinkler')
model.add_edge('sprinkler', 'grass_wet')
model.add_edge('rains', 'grass_wet')
     

p_rains_and_wet = state_prob(model, {'rains': 1, 'grass_wet': 1}, property_='dist')
p_wet = state_prob(model, {'grass_wet': 1}, property_='dist')

p_rains_if_wet = p_rains_and_wet / p_wet
print(p_rains_and_wet, p_wet, p_rains_if_wet)
print(state_prob(model, {'rains': 1, 'grass_wet': 1, 'sprinkler': 1}, property_='dist'))
print(state_prob(model, {}, property_='dist'))

allclose = lambda x, y, atol=1e-8: abs(x-y) < atol

def assert_p_rains_if_wet(p, label):
    expected = 0.36
    try:
        assert allclose(p, expected, atol=0.01)
    except AssertionError as e:
        print('Failure in assert_p_rains_if_wet(label=%s)' % label)
        print('expected =', expected)
        print('observed =', p) # 0.06
        raise e


