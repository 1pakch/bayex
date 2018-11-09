# bayex

Bayex is a Python package implementing directed Bayesian networks over
finitely-supported distributions. It was built to calculate the
likelihoods of recessive diseases in consanguineous families (
[resulting figures](https://github.com/ilya-kolpakov/bayex/blob/dirty/plots/all.pdf).
The package quite unique in that it can calculate probabilities of
interest [*symbolically*](#symbolic-computations) if one uses [SymPy][sympy]
expressions as distribution parameters.

Existing packages such as [pymc3](https://github.com/pymc-devs/pymc3) or
[pomegranate](https://github.com/jmschrei/pomegranate) are focused on
sampling or approximate algorithms which and have little support for
transparent calculations on small networks.

## Example

Let's implement a [example](https://en.wikipedia.org/wiki/Bayesian_network)
of a Bayesian network from Wikipedia:

![Sprinkler network](https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/SimpleBayesNet.svg/575px-SimpleBayesNet.svg.png)

We start by defining the necessary probability distributions. The simplest
one is the distribution for of the event `{it rains}` since it is
*unconditional* (fixed a priori) at 20%:

```py
from bayex import *

# There is a 20% chance that it rains
it_rains = Bernoulli(0.2) 
```

Now we specify the *conditional* distributions. These are defined as
functions (or callables objects) in Python that take the *values* of
conditioning variables as arguments and return *distributions*.
The definition of the conditional distribution of
the event `{sprinkler is on}` should be pretty self-explanatory:

```py
# It it rains there's 1% chance that the sprinkler is on,
# otherwise the sprinkler is on with 40% probability.

def sprinkler_on(rains):
    return Bernoulli(0.01) if rains else Bernoulli(0.4)
```

The conditional distribution of the event `{grass is wet}` depends on the
other two events its definition is a bit longer, but the structure
remains exactly the same. One defines a function that takes conditioning
*variables* and returns a *distribution*:
```py
def grass_wet(sprinkler_on, it_rains):
    if not sprinkler_on and not it_rains:
        return Constant(0)
    elif not sprinkler_on and it_rains:
        return Bernoulli(0.8)
    elif sprinkler_on and not it_rains:
        return Bernoulli(0.9)
    else: # sprinkler_on and it_rains
        return Bernoulli(0.99)
```
Constant is, in effect, a degenerate distribution (the one that has
no variability if you wish).

Now we need to connect the distributions and create out network
(a directed graph in fact). Bayex relies on
[networkx](https://networkx.github.io/) for holding graph structures
(which is admittedly an overkill) so we import it and create a digraph
exactly representing the diagram above:

```py
import networkx as nx

model = nx.DiGraph()

# Add nodes
model.add_node('it_rains', dist=it_rains)
model.add_node('sprinkler_on', dist=sprinkler_on)
model.add_node('grass_wet', dist=grass_wet)

# Create the causality "arrows" (from the first argument to the second one)
model.add_edge('it_rains', 'sprinkler_on')
model.add_edge('sprinkler_on', 'grass_wet')
model.add_edge('it_rains', 'grass_wet')
```
Note that the distributions are passed as keyword arguments to `add_node()`
calls and are actually stored in the same-named attributes.

So far so good. We can now compute the *joint* probability of the event
`{grass wet AND it rains}` and a *marginal* probability of the event
`{grass wet}`:
```py
p_it_rains_and_grass_wet = state_prob(model, {'it_rains': 1, 'grass_wet': 1}, property_='dist')
p_grass_wet = state_prob(model, {'grass_wet': 1}, property_='dist')
```
Again, we pass `"dist"` as an argument so that the `state_prob` function
knows hot to get to the distributions of the nodes. Now we have everything
we need to calculate the *conditional* proability of the event
`{it rains | grass wet}`:
```
p_it_rains_given_grass_wet = p_it_rains_and_grass_wet / p_grass_wet
print(p_it_rains_given_grass_wet)
```
which yields 0.3577. If one observes that the grass is wet it the
odds that it does not rain are roughly 2 to 1.

## Symbolic Computations

A very cool thing that the calculation above works just fine if one
specifies the distribution parameters *symbolically*. For instance:

```py
import sympy

p = sympy.symbol('p')
it_rains = Bernoulli(p)

# ... 

print(p_it_rains_given_grass_wet)
```
yields
```
0.8019*p 0.4419*p + 0.36 0.8019*p/(0.4419*p + 0.36)
```





[sympy]: https://www.sympy.org/
[pymc]: https://github.com/pymc-devs/pymc3
[pomegranate]: https://github.com/jmschrei/pomegranate
