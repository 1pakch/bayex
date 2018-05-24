import networkx as nx

from collections import defaultdict

from distributions import *
from marginalize import *


G = nx.DiGraph()

G.add_node('r', dist=Bernoulli(0.5))
G.add_node('a', dist=Forward1(1))
G.add_node('b', dist=Forward1(1))
G.add_node('s', dist=Sum(2))

G.add_edge('r', 'a')
G.add_edge('r', 'b')
G.add_edge('a', 's')
G.add_edge('b', 's')


result = marginalize(G, 's')
print(Marginal(result))



