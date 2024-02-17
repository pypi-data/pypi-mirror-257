from pathlib import Path as _Path
from random import Random as _Random
from inspect import signature as _signature
from functools import (
    partial as _partial,
    wraps as _wraps,
)
import string as _string
import pickle as _pickle
import os as _os

dump = _partial(_pickle.dump, protocol=_pickle.HIGHEST_PROTOCOL)
dumps = _partial(_pickle.dumps, protocol=_pickle.HIGHEST_PROTOCOL)


def get_valid_kwargs(func, kwargs):
    """Get the subset of non-None ``kwargs`` that are valid params for ``func``"""
    sig_params = list(_signature(func).parameters)
    return {k: v for k, v in kwargs.items() if k in sig_params and v is not None}


def generate_random_weights(xlen, weights):
    if not isinstance(xlen, int):
        if isinstance(xlen, (list, tuple, set, range)):
            xlen = len(xlen)
        else:
            raise TypeError("xlen must be an int representing the length of the desired weights or a sequence of values that length can be obtained from")

    if isinstance(weights[0], float):
        weights = tuple((i, x) for i,x in enumerate(weights))
    elif isinstance(weights[0], int):
        weights = tuple((i, x/100) for i,x in enumerate(weights))
    elif isinstance(weights[0][0], int):
        weights = tuple((x[0], x[1]/100) for x in weights)

    mapping = dict(weights)
    indexes = set(x[0] for x in weights)
    weights = tuple(x[1] for x in weights)
    weight_to_split = 1 - sum(weights)
    assert weight_to_split > 0, "sum of given weights must be less than 1"
    len_of_weights = xlen - len(weights)
    constant = weight_to_split / len_of_weights
    return tuple(constant if i not in indexes else mapping[i] for i in range(xlen))


def make_path(path):
    '''The function "make_path" converts a given path into an instance of the "_Path" class if it is not
    already an instance of that class.

    Parameters
    ----------
    path
        The `path` parameter is the input path that needs to be converted into a `_Path` object.

    Returns
    -------
        the `path` object.

    '''
    if not isinstance(path, _Path):
        path = _Path(path)
    return path


def generate_random_path(suffix="", prefix="", dir="/tmp"):
    '''The function `generate_random_path` generates a random path by combining a prefix, suffix, and
    directory.

    Parameters
    ----------
    suffix
        The "suffix" parameter is an optional string that will be appended to the end of the generated
    random filename. It can be used to specify a file extension or any other desired suffix for the
    filename.
    prefix
        The prefix parameter is an optional string that will be added to the beginning of the generated
    random filename.
    dir, optional
        The `dir` parameter is an optional parameter that specifies the directory where the random path
    will be created. If `dir` is not provided, the random path will be created in the `/tmp` directory
    by default.

    Returns
    -------
        a Path object representing a randomly generated file path.

    '''
    rng = _Random()
    # Generate a random filename
    random_filename = "".join(rng.choices(_string.ascii_letters + _string.digits, k=8))

    # Apply prefix and suffix if provided
    if prefix:
        random_filename = f"{prefix}{random_filename}"
    if suffix:
        random_filename = f"{random_filename}{suffix}"

    # Create a Path object with the optional directory
    if dir:
        random_path = _Path(dir) / random_filename
    else:
        random_path = _Path(random_filename)

    return random_path


def flatten(iterable, ret=list):
    '''The flatten function takes an iterable and returns a flattened version of it, where any nested
    lists, sets, or tuples are recursively flattened as well.

    Parameters
    ----------
    iterable
        The `iterable` parameter is the input collection that you want to flatten. It can be a list, set,
    tuple, or any other iterable object.
    ret
        The "ret" parameter is a function that determines the type of the returned result. By default, it
    is set to the "list" function, which returns a list. However, you can pass any other function as the
    "ret" parameter to change the type of the returned result. For example

    Returns
    -------
        The function `flatten` returns a flattened version of the input `iterable`. The type of the
    returned object depends on the `ret` parameter. By default, it returns a list.

    '''
    result = []
    for item in iterable:
        if isinstance(item, (list, set, tuple)):
            result.extend(flatten(item, ret=ret))
        else:
            result.append(item)
    return ret(result)





def stringify(values):
    '''The `stringify` function takes a list of values and returns a string representation of the values,
    separated by commas.

    Parameters
    ----------
    values
        The parameter "values" is a list of values that you want to convert into a string.

    Returns
    -------
        The function `stringify` returns a string that is the concatenation of all the values in the
    `values` list, separated by commas.

    '''
    return ",".join(str(value) for value in values)


def abs_path(relative=None):
    '''The `abs_path` function returns the absolute path of a file or directory, given a relative path.

    Parameters
    ----------
    relative
        The `relative` parameter is an optional argument that represents a relative path. If provided, it
    will be appended to the current working directory to form an absolute path. If not provided, the
    function will simply return the current working directory as the absolute path.

    Returns
    -------
        The function `abs_path` returns the absolute path of the current working directory if no relative
    path is provided. If a relative path is provided, it returns the absolute path by joining the
    current working directory with the relative path.

    '''
    path = module_dir = _os.getcwd()
    if relative is not None:
        path = _os.path.join(path, relative)
    return path


def format_multiline(*args, lines=None):
    return "\n".join(lines) if lines is not None else "\n".join(args)