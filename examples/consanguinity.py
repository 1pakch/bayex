import pandas as pd

from bayex import marginalize
from bayex.mendelian import unrelated, first_cousins, Genotype


def create_families(default_genotype):
    return (unrelated(default=default_genotype),
            first_cousins(default=default_genotype))

def get_offspring_genotypes(families):
    return {fam.name: fam.infer_genotype('offspring') for fam in families}

def test_symbolic():
    import sympy
    q = sympy.Symbol('q')
    hwg = Genotype.hardy_weinberg(q)
    fams = create_families(hwg)
    simplify = lambda d: {v: sympy.simplify(p) for v, p in d.items()}
    return get_offspring_genotypes(fams)

def test_numeric(q):
    hwg = Genotype.hardy_weinberg(q)
    fams = create_families(hwg)
    gts = get_offspring_genotypes(fams)
    gts = {k: pd.Series(dict(v.items())) for k, v in gts.items()}
    return pd.DataFrame(gts).T


def p_no_disease(p_disease, n):
    return (1-p_disease)**n

def p_at_least_one_disease(p_disease, n):
    return 1 - p_no_disease(p_disease, n)


def main():
    test_symbolic()
    print(test_numeric(0.01))
    return 0

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
    main()
