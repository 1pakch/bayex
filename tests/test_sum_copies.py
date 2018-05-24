import networkx as nx
import bayex as bx

def create_graph():  
    G = nx.DiGraph()
    G.add_node('root', dist=bx.Bernoulli(0.5))
    G.add_node('copy1', dist=lambda x: bx.Constant(x))
    G.add_node('copy2', dist=lambda x: bx.Constant(x))
    G.add_node('sum', dist=lambda x, y: bx.Constant(x+y))
    G.add_edge('root', 'copy1')
    G.add_edge('root', 'copy2')
    G.add_edge('copy1', 'sum')
    G.add_edge('copy2', 'sum')
    return G

def test():
    G = create_graph()
    sum_dist = bx.marginalize(G, 'sum', 'dist')
    assert set(sum_dist.keys()) == set([0,2])
    assert sum_dist[0] == 0.5
    assert sum_dist[2] == 0.5

