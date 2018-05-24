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


def _gen_offspring_genotypes_dist():
    "Distribution of a child's genotype given these of parents (as a dict)"
    table = {}
    # Iterate over possible combinations of parents' genotypes
    for gt_father, gt_mother in product(Genotypes, Genotypes):
        # the list of (equiprobable) child's genotypes given g1 and g2
        gts = map(genotype, product(gt_father, gt_mother))
        # conditional distribution the child genotype given g1 and g2
        dist = {gt: count/4 for gt, count in Counter(gts).items()}
        # store this conditional distribution under g1 and g2
        table[gt_father, gt_mother] = Genotype(dist)
    return table

_cdist = _gen_offspring_genotypes_dist()
def inherit(gt_father, gt_mother):
    "Conditional distribution of a child's genotype given these of parents"
    return _cdist[gt_father, gt_mother]


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

    def add_unrelated(self, name, genotype=None, **kwargs):
        if genotype is None:
            genotype = self.default_genotype
        self.add_node(name, genotype=genotype, **kwargs)
        return name

    def add_child(self, parent1, parent2, name):
        self.add_node(name, genotype=inherit)
        self.add_edge(parent1, name)
        self.add_edge(parent2, name)
        return name

    def add_children(self, parent1, parent2, names):
        for name in names:
            self.add_child(parent1, parent2, name)
        return names

    def infer_genotype(self, name):
        return marginalize(self, name, 'genotype')


def unrelated(name='unrelated', default=None, father=None, mother=None):
    "A family where the offspring's parents are unrelated"
    fam = FamilyTree(name=name, default_genotype=default)
    f = fam.add_unrelated('father', dist=father)
    m = fam.add_unrelated('mother', dist=mother)
    fam.add_child(f, m, 'offspring')
    return fam


def first_cousins(name='first_cousins', default=None):
    "A family where the offspring's parents are first cousins"
    fam = FamilyTree(name=name, default_genotype=default)
    # Shared grandgrandparents
    fam.add_unrelated('ggf')
    fam.add_unrelated('ggm')
    # Share grandparents
    fam.add_children('ggf', 'ggm', ['gp1', 'gp2'])
    # Unrelated grandparents
    fam.add_unrelated('gp1_spouse')
    fam.add_unrelated('gp2_spouse')
    # First cousins that produce offsprings
    fam.add_child('gp1', 'gp1_spouse', 'f')
    fam.add_child('gp2', 'gp2_spouse', 'm')
    # Their offspring
    fam.add_child('f', 'm', 'offspring')
    return fam
