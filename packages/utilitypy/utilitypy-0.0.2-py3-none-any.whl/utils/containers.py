from hashlib import sha256 as _sha256
from pickle import dumps as _dumps
from rbloom import Bloom as _Bloom


def bloom_hash(obj):
    '''The `bloom_hash` function takes an object, hashes it using SHA256, and returns a 128-bit integer.

    Parameters
    ----------
    obj
        The `obj` parameter in the `bloom_hash` function is the object that you want to hash. It can be any
    Python object that can be serialized using the `_dumps` function. The `_dumps` function is not
    defined in the code snippet you provided, so you would need

    Returns
    -------
        The function `bloom_hash` returns an integer value.

    '''
    h = _sha256(_dumps(obj)).digest()
    return int.from_bytes(h[:16], "big") - 2**127


def bloomfilter(n_items=1_000_000, fp_rate=0.01, hash_fn=bloom_hash):
    '''The `bloomfilter` function returns an instance of the `_Bloom` class with specified parameters for
    the number of items, false positive rate, and hash function.

    Parameters
    ----------
    n_items, optional
        The number of items that the Bloom filter is expected to store. This parameter determines the size
    of the Bloom filter's bit array.
    fp_rate
        The false positive rate is the probability that the bloom filter incorrectly reports an item as
    being in the set when it is not.
    hash_fn
        The `hash_fn` parameter is a function that is used to generate hash values for the items being
    inserted into the Bloom filter. The default value for `hash_fn` is `bloom_hash`, which is likely a
    custom hash function specifically designed for Bloom filters.

    Returns
    -------
        The function `bloomfilter` returns an instance of the `_Bloom` class.

    '''
    return _Bloom(n_items, fp_rate, hash_fn)