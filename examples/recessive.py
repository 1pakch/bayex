import pandas as pd
import sympy
from pprint import pprint

from bayex import marginalize
from bayex.mendelian import Genotype
import bayex.families as fam


generators = [
    fam.siblings,
    fam.sibling_cousins,
    fam.half_siblings,
    fam.first_cousins,
    fam.half_first_cousins,
    fam.second_cousins,
    fam.unrelated
]

def create_families(default):
    return [ffunc(default=default) for ffunc in ffuncs]

def calculate_offspring_genotypes(q):
    g = Genotype({'AA': 1 - q, 'Aa': q})
    families = [f(default=g) for f in generators]
    return {fam.cofficient_of_relationship:
            fam.infer_genotype('offspring') for fam in families}

def p_no_disease(p_disease, n):
    return (1-p_disease)**n

def p_at_least_one_disease(p_disease, n):
    return 1 - p_no_disease(p_disease, n)


def main():
    qval = 0.01
    d = dict()
    d['num'] = calculate_offspring_genotypes(q=qval)

    qsym = sympy.Symbol('q')
    d['sym'] = calculate_offspring_genotypes(q=qsym)
    d['sym'] = {k: dist.simplify() for k, dist in d['sym'].items()}
    d['eval'] = {k: dist.eval({qsym: qval}) for k, dist in d['sym'].items()}

    d = {k: pd.DataFrame(v) for k, v in d.items()}

    return d

    import sys
    n = 1800
    if len(sys.argv) == 1:
        qs = [0.1, 0.01, 0.0001]
    else:
        qs = map(float, sys.argv[1:])

    for q in qs:
        fams = create_families(Genotype.hardy_weinberg(q))

        so, fco = test(q)
        p_aa_so = so._vpdict['aa']
        p_aa_fco = fco._vpdict['aa']
        p1_so = p_at_least_one_disease(p_aa_so, n=n)
        p1_fco = p_at_least_one_disease(p_aa_fco, n=n)
        print('Minor allele frequency = %g' % q )
        print('Offspring distr (unrelated)     = %s' % str(so))
        print('Offspring distr (first cousins) = %s' % str(fco))
        print('Allele <aa> x%.2f times more frequent in first cousins\' offsprings' % (p_aa_fco / p_aa_so))
        print('P(n_diseases>0| n=%d) (unrelated)     = %s' % (n, p1_so))
        print('P(n_diseases>0| n=%d) (first cousins) = %s' % (n, p1_fco))
        print('Increase by x%.2f times in first cousins\' offsprings' % (p1_fco / p1_so))
        print()

if __name__ == '__main__':
    d = main()
