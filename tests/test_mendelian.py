from bayex.mendelian import *
from bayex.families import *


def test_unrelated_hw():
    'Hardy-Weinberg equilibrium is preserved through unrelated mating'
    q = 0.4
    gtp = Genotype.hardy_weinberg(q)
    fam = unrelated(default=gtp)
    gto = fam.infer_genotype('offspring')
    for k in Genotypes:
        assert abs(gtp[k] - gto[k]) < 1e-4
