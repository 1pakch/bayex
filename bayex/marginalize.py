import networkx as nx
import collections

from .distributions import Marginal


dict0 = lambda: collections.defaultdict(lambda: 0)

def _marginalize(G, topo, node, property_, values={}):
    cur = topo[0]
    inputs = [values[node] for node in G.predecessors(cur)]
    conditional = G.node[cur][property_](*inputs)
    if cur == node:
        return conditional
    else:
        result = dict0()
        values_ = values.copy()
        for v, p in conditional.items():
            values_[cur] = v
            result_ = _marginalize(G, topo[1:], node, property_, values_)
            for vr, pr in result_.items():
                result[vr] += pr * p
        return result

def marginalize(G, node, property_):
    topo = list(nx.topological_sort(G))
    if not node in G.nodes.keys():
        raise ValueError("marginalize(): no node '{:s}' in graph '{:s}'"
                         .format(node, G.name))
    return Marginal(_marginalize(G, topo, node, property_))
