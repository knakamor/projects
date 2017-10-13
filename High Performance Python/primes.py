import math
import multiprocessing
import itertools
from timeit import Timer

def check_prime(n):
    """Checks if a number is prime.

    Parameters
    ----------
    n: an Int

    Returns
    -------
    Bool
    """
    if n % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def primes_sequential(number_range):
    """Finds all primes in a sequence.

    Parameters
    ----------
    number_range: an iterable of ints

    Returns
    -------
    list of primes
    """
    primes = []
    for possible_prime in number_range:
        if check_prime(possible_prime):
            primes.append(possible_prime)
    return primes


def head_tail(primes):
    """Prints first and last 10 entries from a list (of primes here).
    This lets us see the output from our various jobs.

    Parameters
    ----------
    primes: a list

    Returns
    -------
    None. Side effect is print to stdout.
    """
    print len(primes), primes[:10], primes[-10:]


def primes_parallel(number_range):
    """Computes primes in parallel using multiprocessing.

    Parameters
    ----------
    number_range: an iterable of ints to check for primeness.

    Returns
    -------
    list of primes
    """

    pool = multiprocessing.Pool(processes=4)
    outputs = pool.map(check_prime, number_range)
    return outputs

if __name__ == "__main__":
    # number_range = xrange(10, 20)
    number_range = xrange(100000000, 101000000)
    # Make a list of functions to time.
    # callables without args...
    funcs = [primes_sequential, primes_parallel]
    tests = [(test_func.__name__, test_func) for test_func in funcs]

    for name, test in tests:
        # We have to do this because Timer takes a callable as an arg.
        t = Timer(lambda: head_tail(test(number_range)))
        print "Completed {name} in {time} seconds.".format(name=name,
                                                           time=t.timeit(1))
