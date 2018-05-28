import networkx as nx
import collections

from .distributions import Marginal, Constant


def _state_prob(G, tail, knowns, property_, **values):
    if not tail:
        return 1
    cur = tail[0]
    inputs = [values[node] for node in G.predecessors(cur)]
    conditional = G.node[cur][property_](*inputs)
    prob = 0
    for v, p in conditional.items():
        if cur in knowns and knowns[cur] != v:
            continue
        values[cur] = v
        tail_prob = _state_prob(G, tail[1:], knowns, property_, **values)
        prob += p * tail_prob
    return prob

def state_prob(G, knowns, property_):
    tail = list(nx.topological_sort(G))
    return _state_prob(G, tail, knowns, property_)
