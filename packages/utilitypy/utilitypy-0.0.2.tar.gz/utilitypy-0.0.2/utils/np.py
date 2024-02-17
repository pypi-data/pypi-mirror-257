import numpy as _numpy


def rng():
    '''The function `rng()` returns a random number generator using the default random number generator
    from the NumPy library.

    Returns
    -------
        The function `rng()` returns a random number generator object from the NumPy library.

    '''
    return _numpy.random.default_rng(_numpy.random.SeedSequence().entropy)
