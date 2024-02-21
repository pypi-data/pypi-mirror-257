from __future__ import annotations

import numpy as np
from sklearn.utils import check_array as skl_check_array

T_DEFAULT = object()


def validate_input(x, t=T_DEFAULT):
    if not isinstance(x, np.ndarray) and not isinstance(x, list):
        raise ValueError("x must be array-like OR a list of array-like")
    elif isinstance(x, list):
        for i in range(len(x)):
            x[i] = validate_input(x[i], t)
        return x
    elif x.ndim == 1:
        x = x.reshape(-1, 1)
    x = check_array(x)

    # add another case if x is a list of trajectory

    if t is not T_DEFAULT:
        if t is None:
            raise ValueError("t must be a scalar or array-like.")
        # Apply this check if t is a scalar
        elif np.ndim(t) == 0 and (isinstance(t, int) or isinstance(t, float)):
            if t <= 0:
                raise ValueError("t must be positive")
        # Only apply these tests if t is array-like
        elif isinstance(t, np.ndarray):
            if not len(t) == x.shape[0]:
                raise ValueError("Length of t should match x.shape[0].")
            if not np.all(t[:-1] < t[1:]):
                raise ValueError("Values in t should be in strictly increasing order.")
        else:
            raise ValueError("t must be a scalar or array-like.")

    return x


def check_array(x, **kwargs):
    if np.iscomplexobj(x):
        return skl_check_array(x.real, **kwargs) + 1j * skl_check_array(
            x.imag, **kwargs
        )
    else:
        return skl_check_array(x, **kwargs)


def drop_nan_rows(arr, *args):
    """
    Remove rows in all inputs for which `arr` has `_np.nan` entries.

    Parameters
    ----------
    arr : numpy.ndarray
        Array whose rows are checked for nan entries.
        Any rows containing nans are removed from ``arr`` and all arguments
        passed via ``args``.
    *args : variable length argument list of numpy.ndarray
        Additional arrays from which to remove rows.
        Each argument should have the same number of rows as ``arr``.

    Returns
    -------
    arrays : tuple of numpy.ndarray
        Arrays with nan rows dropped.
        The first entry corresponds to ``arr`` and all following entries
        to ``*args``.
    """
    nan_inds = np.isnan(arr).any(axis=1)
    return (arr[~nan_inds], *[arg[~nan_inds] for arg in args])
