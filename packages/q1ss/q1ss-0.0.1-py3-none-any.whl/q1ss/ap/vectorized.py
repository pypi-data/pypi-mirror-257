"""
Vectorised versions of affine partition operations.
"""

# Part of: q1ss
# Copyright (C) 2023 Hashberg Ltd and 20squares UG

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301
# USA

from __future__ import annotations
from typing import Sequence, TypeVar
import numpy as np
from ..binalg.vectorized import BinMat, BinVec


def sequence_ap_label(
    n: int,
    k: int,
    start: BinMat,
    mats0: Sequence[BinMat],
    mats1: Sequence[BinMat],
    vec: BinVec,
) -> BinVec:
    """
    Computes the label assigned to a binary vector ``vec`` by a sequence-based
    affine partition with ambient dimension ``n``, label dimension ``k``,
    as well as given ``start`` matrix and matrix sequence ``mats``.
    """
    vec = (start @ vec) % 2  # type: ignore
    for i in range(k - 1):
        if vec[-1 - i]:
            vec[: n - i - 1] = (mats1[i] @ vec[: n - i - 1]) % 2
        else:
            vec[: n - i - 1] = (mats0[i] @ vec[: n - i - 1]) % 2
    return vec[-1 : -1 - k : -1]


# For numba on Python 3.12,
# see: numba.discourse.group/t/ann-numba-0-59-0rc1-and-llvmlite-0-42-0rc1/2329
try:
    # If Numba is available, JIT compile all low-level functions:
    import numba  # type: ignore

    _FuncT = TypeVar("_FuncT")

    def _numba_compile(func: _FuncT) -> _FuncT:
        return numba.jit(nopython=True, cache=True)(func)  # type: ignore

    @_numba_compile
    def _sequence_ap_label(
        n: int,
        k: int,
        start: BinMat,
        mats0: Sequence[BinMat],
        mats1: Sequence[BinMat],
        vec: BinVec,
    ) -> BinVec:
        """
        Numba-friendly version of :func:`sequence_ap_label`, replacing @
        with explicit loops, vectorised products and sums.
        """
        vec = vec.copy()
        _vec = np.zeros(n, dtype=np.uint8)
        for j in range(n):
            _vec[j] = np.sum(start[j] * vec) % 2
        vec[:n] = _vec
        for i in range(k - 1):
            if vec[-1 - i]:
                for j in range(n - i - 1):
                    _vec[j] = np.sum(mats1[i][j] * vec[: n - i - 1]) % 2
            else:
                for j in range(n - i - 1):
                    _vec[j] = np.sum(mats0[i][j] * vec[: n - i - 1]) % 2
            vec[: n - i - 1] = _vec[: n - i - 1]
        return vec[-1 : -1 - k : -1]

    def _wrapped_sequence_ap_label(
        n: int,
        k: int,
        start: BinMat,
        mats0: Sequence[BinMat],
        mats1: Sequence[BinMat],
        vec: BinVec,
    ) -> BinVec:
        """
        Wraps :class:`~collections.abc.Sequence` into ``numba.typed.List``
        to deal with deprecation of reflection for lists and set types in numba:
        https://numba.readthedocs.io/en/stable/reference/deprecation.html#deprecation-of-reflection-for-list-and-set-types
        """
        mats0 = numba.typed.List(mats0)
        mats1 = numba.typed.List(mats1)
        return _sequence_ap_label(n, k, start, mats0, mats1, vec)

    sequence_ap_label = _wrapped_sequence_ap_label

except ModuleNotFoundError:
    numba = None
