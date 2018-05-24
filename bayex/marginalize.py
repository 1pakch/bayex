import networkx as nx
import collections

from .distributions import Marginal


dict0 = lambda: collections.defaultdict(lambda: 0)

def _marginalize(G, topo, node, property_, **values):
    cur = topo[0]
    inputs = [values[node] for node in G.predecessors(cur)]
    conditional = G.node[cur][property_](*inputs)
    if cur == node:
        return conditional
    else:
        mixture = []
        for v, p in conditional.items():
            values[cur] = v
            cdist = _marginalize(G, topo[1:], node, property_, **values)
            mixture.append((cdist, p))
        return Marginal.from_mixture(mixture)

def marginalize(G, node, property_):
    topo = list(nx.topological_sort(G))
    if not node in G.nodes.keys():
        raise ValueError("marginalize(): no node '{:s}' in graph '{:s}'"
                         .format(node, G.name))
    return Marginal(_marginalize(G, topo, node, property_))
