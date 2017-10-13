"""
Objects useful for sampling from basic distributions.
Each of these objects is a simple wrapper around a function in numpy.random,
they simply change the API.  Instead of functions that take parameters *and*
vectors, we create objects from parameters at initialization time.  The created
objects then have a method `sample` which returns iid samples from the given
distribution.
"""
import numpy as np
import numpy.random as rnd
import scipy.stats as stats


class Uniform(object):

    def __init__(self, a, b):
        self._a = a
        self._b = b

    def sample(self, n):
        return rnd.uniform(low=self._a, high=self._b, size=n)

    def pdf(self, t):
        return stats.uniform.pdf(t, loc=self._a, scale=(self._b - self._a))

    def cdf(self, t):
        return stats.uniform.cdf(t, loc=self._a, scale=(self._b - self._a))


class Exponential(object):

    def __init__(self, a):
        self._a = a

    def sample(self, n):
        return rnd.exponential(scale=self._a, size=n)

    def pdf(self, t):
        return stats.expon.pdf(t, scale=(1/float(self._a)))

    def cdf(self, t):
        return stats.expon.cdf(t, scale=(1/float(self._a)))


class Normal(object):

    def __init__(self, mu, sigma):
        self._mu = mu
        self._sigma = sigma

    def sample(self, n):
        return rnd.normal(loc=self._mu, scale=self._sigma, size=n)

    def pdf(self, t):
        return stats.norm.pdf(t, loc=self._mu, scale=self._sigma)

    def cdf(self, t):
        return stats.norm.cdf(t, loc=self._mu, scale=self._sigma)

    def percentile(self, t):
        return stats.norm.ppf(t, loc=self._mu, scale=self._sigma)


class Poisson(object):

    def __init__(self, lam):
        self._lam = lam

    def sample(self, n):
        return rnd.poisson(lam=self._lam, size=n)


class Binomial(object):

    def __init__(self, n, p):
        self._n = n
        self._p = p

    def sample(self, n):
        return rnd.binomial(n=self._n, p=self._p, size=n)

    def pdf(self, t):
        return stats.binom.pmf(t, self._n, self._p)

    def cdf(self, t):
        return stats.binom.cdf(t, self._n, self._p)


class Students(object):

    def __init__(self, df):
        self._df = df

    def sample(self, n):
        return rnd.standard_t.sample(df=self._df, size=n)

    def pdf(self, t):
        return stats.t.pdf(t, self._df)

    def cdf(self, t):
        return stats.t.cdf(t, self._df)


class ChiSquared(object):

    def __init__(self, df):
        self._df = df

    def pdf(self, t):
        return stats.chi2.pdf(t, self._df)

    def cdf(self, t):
        return stats.chi2.cdf(t, self._df)


def sample_from_sum(n, *samplers):
    """Sample from the sum of a varaible number of random varaibles."""
    n_samplers = len(samplers)
    samples = np.empty(shape=(n, n_samplers))
    for i, sampler in enumerate(samplers):
        samples[:, i] = sampler.sample(n)
    return np.sum(samples, axis=1)


def sample_from_repeated_sum(n_samples, n_summands, sampler):
    """Sample n_samples from the sum of n_summands iid copies of a random
    varaible.
    """
    samples = sampler.sample(n_samples*n_summands).reshape(n_samples, n_summands)
    return np.sum(samples, axis=1)


def sample_means_from_population(n_samples, n_summands, sampler):
    return (1.0/n_summands) * sample_from_repeated_sum(n_samples, n_summands, sampler)

def secret_data():
    normal = Normal(0.1, 0.7)
    data = normal.sample(50)
    return data
