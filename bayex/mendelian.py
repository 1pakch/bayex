import networkx as nx
from collections import Counter
from itertools import product

from .distributions import Marginal
from .marginalize import marginalize


Alleles = ('A', 'a')
Genotypes = ('AA', 'Aa', 'aa')

_genotype = {
    ('A', 'A'): 'AA',
    ('A', 'a'): 'Aa',
    ('a', 'A'): 'Aa',
    ('a', 'a'): 'aa',
}

def genotype(alleles_tuple):
    return _genotype[alleles_tuple]


class Genotype(Marginal):

    #def __init__(self, probabilities):
    #    Marginal.__init__(self, dict(zip(Alleles, probabilities)))

    @staticmethod
    def certain(genotype):
        return Genotype({genotype: 1})

    @staticmethod
    def hardy_weinberg(p_minor_allele):
        "Genotype distribution in the Hardy-Weinberg equilibrium"
        q = p_minor_allele
        p = 1 - q
        return Genotype({'AA': p**2, 'Aa': 2*p*q, 'aa': q**2})


def _gen_offspring_genotypes_dist(aa=True):
    "Distribution of a child's genotype given these of parents (as a dict)"
    table = {}
    # Iterate over possible combinations of parents' genotypes
    for gt_father, gt_mother in product(Genotypes, Genotypes):
        # the list of (equiprobable) child's genotypes given g1 and g2
        gts = [genotype((fg, mg)) for fg, mg in product(gt_father, gt_mother)]
        # Remove aa 
        if not aa:
            gts = [gt for gt in gts if not gt == 'aa']
        n = len(gts)
        # conditional distribution the child genotype given g1 and g2
        dist = {gt: count/n for gt, count in Counter(gts).items()}
        # store this conditional distribution under g1 and g2
        table[gt_father, gt_mother] = Genotype(dist)
    return table

_cdist1 = _gen_offspring_genotypes_dist(aa=True)
def inherit(gt_father, gt_mother):
    "Conditional distribution of a child's genotype given these of parents"
    return _cdist1[gt_father, gt_mother]

_cdist2 = _gen_offspring_genotypes_dist(aa=False)
def inherit_no_aa(gt_father, gt_mother):
    "Conditional distribution of a child's genotype given these of parents"
    return _cdist2[gt_father, gt_mother]


class FamilyTree(nx.DiGraph):

    def __init__(self, name=None, default_genotype=None):
        "A family tree for modelling mendelian traits"
        nx.DiGraph.__init__(self)
        self.name = str(name)
        self._default_genotype = default_genotype

    def __repr__(self):
        return 'Family(name={:s})'.format(self.name)

    def _exception(self, reason, type_=ValueError):
        return type_('{:s}: {:s}.'.format(repr(self), reason))

    @property
    def default_genotype(self):
        if self._default_genotype is None:
            raise self._exception('default allele distribution is not set')
        return self._default_genotype

    def _name(self):
        return str(self.number_of_nodes())

    def add_unrelated(self, name=None, **kwargs):
        return self.add_unrelateds([name])[0]
    
    def add_unrelateds(self, names=[None, None], **kwargs):
        _names = []
        for name in names:
            if name is None:
                name = self._name()
            self.add_node(name, genotype=self._default_genotype, **kwargs)
            _names.append(name)
        return _names

    def add_child(self, parent1=None, parent2=None, name=None, inherit=inherit):
        return self.add_children(parent1, parent2, [name], inherit=inherit)[0]

    def add_children(self, parent1=None, parent2=None, names=[None, None],
                     inherit=inherit):
        if parent1 is None:
            parent1 = self.add_unrelated()
        if parent2 is None:
            parent2 = self.add_unrelated()
        _names = []
        for name in names:
            if name is None:
                name = self._name()
            self.add_node(name, genotype=inherit)
            self.add_edge(parent1, name)
            self.add_edge(parent2, name)
            _names.append(name)
        return _names

    def infer_genotype(self, name):
        return marginalize(self, name, 'genotype')



