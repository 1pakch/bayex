"Marginal and conditional distributions with finite support"

import abc


class Marginal:

    def __init__(self, vpdict):
        self._vpdict = vpdict

    def items(self):
        return self._vpdict.items()

    def __getitem__(self, v):
        return self._vpdict[v]

    def __call__(self, *args):
        return self

    def __eq__(self, other):
        return self._vpdict == other._vpdict

    def __str__(self):
        vp = sorted(self.items(), key=lambda t: t[0])
        vs = [str(v) for v, p in vp]
        ps = ['{:<8.4g}'.format(p) for v, p in vp]
        s = ', '.join(('%s: %s'%(v, p) for v, p in zip(vs, ps)))
        return 'd{' + s + '}'


class Constant(Marginal):

    def __init__(self, value):
        Marginal.__init__(self, {value: 1})


class Bernoulli(Marginal):

    def __init__(self, p_success, values=(0, 1)):
        probs = (1 - p_success, p_success)
        vpdict = {v: p for p, v in zip(probs, values)}
        Marginal.__init__(self, vpdict)


class Uniform(Marginal):

    def __init__(self, values):
        n = len(values)
        probs = [1 / n] * n
        vpdict = {v: p for p, v in zip(probs, values)}
        Marginal.__init__(self, vpdict)


class Conditional(metaclass=abc.ABCMeta):

    def __init__(self, n_conditioning_variables):
        self._n = n_conditioning_variables

    @abc.abstractmethod
    def __call__(*conditioning_variables):
        "Return a marginal distribution from here"




class Forward(Conditional):

    def __call__(self, *args):
        return Marginal({args: 1})

class Forward1(Conditional):

    def __call__(self, arg):
        return Marginal({arg: 1})

class Sum(Conditional):

    def __call__(self, *args):
        return Marginal({sum(args): 1})

