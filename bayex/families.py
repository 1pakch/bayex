from .mendelian import Genotype, FamilyTree, inherit_no_aa, inherit


def clones(name='clones', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    fam.add_node('x', genotype=default)
    fam.add_node('p1', genotype=lambda x: Genotype.certain(x))
    fam.add_node('p2', genotype=lambda x: Genotype.certain(x))
    fam.add_edge('x', 'p1')
    fam.add_edge('x', 'p2')
    o = fam.add_child('p1', 'p2', 'offspring')
    fam.cofficient_of_relationship = 1
    return fam

def parent_child(name='parent_child', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    p1 = fam.add_unrelated()
    p2 = fam.add_child(p1)
    o = fam.add_child(p1, p2, 'offspring')
    fam.cofficient_of_relationship = 0.5
    return fam

def siblings(name='siblings', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    parents = fam.add_children(names=[None, None], inherit=inherit_no_aa)
    fam.add_child(parents[0], parents[1], 'offspring')
    fam.cofficient_of_relationship = 0.5
    return fam

def sibling_cousins(name='siblings_cousins', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    sibling_gparents = fam.add_children(names=[None, None], inherit=inherit_no_aa)
    gparent2 = fam.add_unrelated()
    parent1 = fam.add_child(sibling_gparents[0], gparent2, inherit=inherit_no_aa)
    parent2 = fam.add_child(sibling_gparents[1], gparent2, inherit=inherit_no_aa)
    fam.add_child(parent1, parent2, 'offspring')
    fam.cofficient_of_relationship = 0.375
    return fam

def grandparent_child(name='grandparent_child', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    ggp = p1 = fam.add_unrelated()
    gp = fam.add_child(ggp, inherit=inherit_no_aa)
    p2 = fam.add_child(gp, inherit=inherit_no_aa)
    fam.add_child(p1, p2, 'offspring')
    fam.cofficient_of_relationship = 0.25
    return fam

def half_siblings(name='half_siblings', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    gps = fam.add_unrelateds([None]*3)
    p1 = fam.add_child(gps[0], gps[2], inherit=inherit_no_aa)
    p2 = fam.add_child(gps[1], gps[2], inherit=inherit_no_aa)
    fam.add_child(p1, p2, 'offspring')
    fam.cofficient_of_relationship = 0.25
    return fam

def first_cousins(name='first_cousins', default=None):
    "A family where the offspring's parents are first cousins"
    fam = FamilyTree(name=name, default_genotype=default)
    # Sibling grandparents
    gps = fam.add_children(names=[None, None], inherit=inherit_no_aa)
    # First cousins that produce offsprings
    p1 = fam.add_child(gps[0], inherit=inherit_no_aa)
    p2 = fam.add_child(gps[1], inherit=inherit_no_aa)
    # Their offspring
    fam.add_child(p1, p2, 'offspring', inherit=inherit)
    fam.cofficient_of_relationship = 0.125
    return fam

def half_first_cousins(name='half_first_cousins', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    # Half-shared grandgrandparents
    ggp = fam.add_unrelateds([None]*3)
    gp1 = fam.add_child(ggp[0], ggp[2], inherit=inherit_no_aa)
    gp2 = fam.add_child(ggp[1], ggp[2], inherit=inherit_no_aa)
    # Left tree
    p1 = fam.add_child(gp1, inherit=inherit_no_aa)
    # Left tree
    p2 = fam.add_child(gp2, inherit=inherit_no_aa)
    # Their offspring
    fam.add_child(p1, p2, 'offspring', inherit=inherit)
    fam.cofficient_of_relationship = 0.0625
    return fam

def second_cousins(name='second_cousins', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    # Sibling grandgrandparents
    ggps = fam.add_children(names=[None]*2)
    gp1 = fam.add_child(ggps[0], inherit=inherit_no_aa)
    gp2 = fam.add_child(ggps[1], inherit=inherit_no_aa)
    p1 = fam.add_child(gp1, inherit=inherit_no_aa)
    p2 = fam.add_child(gp2, inherit=inherit_no_aa)
    fam.add_child(p1, p2, 'offspring', inherit=inherit)
    fam.cofficient_of_relationship = 0.03125
    return fam

def half_second_cousins(name='half_second_cousins', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    # Half-shared grandgrandparents
    gggp = fam.add_unrelateds([None]*3)
    ggp1 = fam.add_child(gggp[0], gggp[2], inherit=inherit_no_aa)
    ggp2 = fam.add_child(gggp[1], gggp[2], inherit=inherit_no_aa)
    gp1 = fam.add_child(ggp1, inherit=inherit_no_aa)
    gp2 = fam.add_child(ggp2, inherit=inherit_no_aa)
    p1 = fam.add_child(gp1, inherit=inherit_no_aa)
    p2 = fam.add_child(gp2, inherit=inherit_no_aa)
    fam.add_child(p1, p2, 'offspring', inherit=inherit)
    fam.cofficient_of_relationship = 0.03125 / 2
    return fam

def third_cousins(name='second_cousins', default=None):
    fam = FamilyTree(name=name, default_genotype=default)
    # Sibling grandgrandparents
    gggps = fam.add_children(names=[None]*2)
    ggp1 = fam.add_child(gggps[0], inherit=inherit_no_aa)
    ggp2 = fam.add_child(gggps[1], inherit=inherit_no_aa)
    gp1 = fam.add_child(ggp1, inherit=inherit_no_aa)
    gp2 = fam.add_child(ggp2, inherit=inherit_no_aa)
    p1 = fam.add_child(gp1, inherit=inherit_no_aa)
    p2 = fam.add_child(gp2, inherit=inherit_no_aa)
    fam.add_child(p1, p2, 'offspring', inherit=inherit)
    fam.cofficient_of_relationship = 0.03125 / 4
    return fam

def unrelated(name='unrelated', default=None):
    "A family where the offspring's parents are unrelated"
    fam = FamilyTree(name=name, default_genotype=default)
    fam.add_child(name='offspring')
    fam.cofficient_of_relationship = 0.0
    return fam
