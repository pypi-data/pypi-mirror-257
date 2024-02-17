"""
    Implementation of binary linear algebra primitives.
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
from numbers import Integral
from typing import Any, Sequence, TypeVar
import numpy as np
import numpy.typing as npt
from ..utils import options

UInt8Vec = npt.NDArray[np.uint8]
"""
Type alias for a NumPy vector of 8-bit unsigned integer type.
"""

BinVec = npt.NDArray[np.uint8]
"""
Type alias for a NumPy vector of 8-bit unsigned integer type,
whose values must all be 0 or 1.
"""

BinMat = npt.NDArray[np.uint8]
"""
Type alias for a NumPy matrix of 8-bit unsigned integer type,
whose values must all be 0 or 1.
"""

BinVecOrMat = npt.NDArray[np.uint8]
"""
Type alias for a NumPy vector or matrix of 8-bit unsigned integer type,
whose values must all be 0 or 1.
"""

BinTensor = npt.NDArray[np.uint8]
"""
Type alias for a NumPy tensor of 8-bit unsigned integer type,
whose values must all be 0 or 1.
"""

IntVec = npt.NDArray[np.integer[Any]]
"""
Type alias for a NumPy vector of arbitrary integer type..
"""


def pivot_idx(vec: BinVec, n: int) -> int:
    """
    Returns the index of the first non-zero entry of the given vector.
    If the first ``n`` entries are all zero, returns ``n``.
    """
    for r in range(n):
        if vec[r]:
            return r
    return n


def _rcef_swap_pivot_col(
    data: BinMat, c: int, num_rows: int, num_cols: int
) -> int:
    swap_c, pivot = c, pivot_idx(data[:, c], num_rows)
    for _c in range(c + 1, num_cols):
        _pivot = pivot_idx(data[:, _c], num_rows)
        if _pivot < pivot:
            swap_c, pivot = _c, _pivot
    if swap_c != c:
        data[:, c], data[:, swap_c] = data[:, swap_c], data[:, c].copy()
    return pivot


def _rcef_clear_pivot_row(
    data: BinMat, c: int, pivot: int, num_cols: int
) -> None:
    col = data[:, c]
    for _c in range(num_cols):
        if _c == c:
            continue
        if data[pivot, _c]:
            data[:, _c] ^= col


def rcef(data: BinMat, ext: bool) -> tuple[BinMat, int]:
    """
    Given the ``data`` of a binary matrix, returns the matrix's RCEF and rank
    ``(rcef_data, rank)``, computed using Gaussian elimination.
    If ``ext`` is set to :obj:`True`, the matrix is first augmented to the
    bottom by the identity matrix with the same number of rows.
    """
    num_rows, num_cols = data.shape
    data = np.copy(data)
    if ext:
        data = np.vstack((data, np.eye(num_cols, dtype=np.uint8)))
    for c in range(num_cols):
        pivot = _rcef_swap_pivot_col(data, c, num_rows, num_cols)
        if pivot == num_rows:
            return data, c
        _rcef_clear_pivot_row(data, c, pivot, num_cols)
    return data, num_cols


def _rref_swap_pivot_row(
    data: BinMat, r: int, num_rows: int, num_cols: int
) -> int:
    swap_r, pivot = r, pivot_idx(data[r], num_cols)
    for _r in range(r + 1, num_rows):
        _pivot = pivot_idx(data[_r], num_cols)
        if _pivot < pivot:
            swap_r, pivot = _r, _pivot
    if swap_r != r:
        data[r], data[swap_r] = data[swap_r], data[r].copy()
    return pivot


def _rref_clear_pivot_col(
    data: BinMat, r: int, pivot: int, num_rows: int
) -> None:
    row = data[r]
    for _r in range(num_rows):
        if _r == r:
            continue
        if data[_r, pivot]:
            data[_r] ^= row


def rref(data: BinMat, ext: bool) -> tuple[BinMat, int]:
    """
    Given the ``data`` of a binary matrix, returns the matrix's RREF and rank
    ``(rref_data, rank)``, computed using Gaussian elimination.
    If ``ext`` is set to :obj:`True`, the matrix is first augmented to the
    right by the identity matrix with the same number of rows.
    """
    # t_rcef, rank = rcef(data.T, ext)
    # return t_rcef.T, rank
    num_rows, num_cols = data.shape
    data = np.copy(data)
    if ext:
        data = np.hstack((data, np.eye(num_rows, dtype=np.uint8)))
    for r in range(num_rows):
        pivot = _rref_swap_pivot_row(data, r, num_rows, num_cols)
        if pivot == num_cols:
            return data, r
        _rref_clear_pivot_col(data, r, pivot, num_rows)
    return data, num_rows


def num_rcef_params(n: int, m: int, pivot_rows: IntVec) -> int:
    """
    Returns the number of free binary parameters for an ``n``-by-``m`` matrix
    in RCEF form with the given pivot rows.
    The pivot rows must be in strict ascending order and in ``range(n)``.
    """
    pivot_cols = np.arange(len(pivot_rows))
    _pivot_rows = np.hstack((pivot_rows, np.array([n])))
    empty_rows = (_pivot_rows[1:] - _pivot_rows[:-1]) - 1
    return int(np.sum(empty_rows * (pivot_cols + 1)))


def num_rref_params(n: int, m: int, pivot_cols: IntVec) -> int:
    """
    Returns the number of free binary parameters for an ``n``-by-``m`` matrix
    in RREF form with the given pivot columns.
    The pivot columns must be in strict ascending order and in ``range(m)``.
    """
    # return num_rcef_params(m, n, pivot_cols)
    pivot_rows = np.arange(len(pivot_cols))
    _pivot_cols = np.hstack((pivot_cols, np.array([m])))
    empty_cols = (_pivot_cols[1:] - _pivot_cols[:-1]) - 1
    return int(np.sum(empty_cols * (pivot_rows + 1)))


def make_rcef(n: int, m: int, pivot_rows: IntVec, params: BinVec) -> BinMat:
    """
    Constructs an ``n``-by-``m`` matrix in RCEF form with the given pivot
    rows and using the given bitvector to set the free binary parameters.
    The pivot rows must be in strict ascending order and in ``range(n)``,
    and the ``params`` vector must have the number of entries given by
    :func:`num_rcef_params`.
    """
    pivot_cols = np.arange(len(pivot_rows))
    _data = np.zeros((n, m), dtype=np.uint8)
    for r, c in zip(pivot_rows, pivot_cols):
        _data[r, c] = 1
    if not np.all(params == 0):
        _pivot_rows = np.hstack((pivot_rows, np.array([n], dtype=np.uint8)))
        empty_cols = (_pivot_rows[1:] - _pivot_rows[:-1]) - 1
        idx = 0
        for r, c, e in zip(pivot_rows, pivot_cols, empty_cols):
            w = e * (c + 1)
            _data[r + 1 : r + 1 + e, 0 : c + 1] = params[idx : idx + w].reshape(
                e, c + 1
            )
            idx += w
    return _data


def make_rref(n: int, m: int, pivot_cols: IntVec, params: BinVec) -> BinMat:
    """
    Constructs an ``n``-by-``m`` matrix in RREF form with the given pivot
    cols and using the given bitvector to set the free binary parameters.
    The pivot cols must be in strict ascending order and in ``range(m)``,
    and the ``params`` vector must have the number of entries given by
    :func:`num_rref_params`.
    """
    # return make_rcef(m, n, pivot_cols, params).T
    pivot_rows = np.arange(len(pivot_cols))
    _data = np.zeros((n, m), dtype=np.uint8)
    for r, c in zip(pivot_rows, pivot_cols):
        _data[r, c] = 1
    if not np.all(params == 0):
        _pivot_cols = np.hstack((pivot_cols, np.array([m], dtype=np.uint8)))
        empty_rows = (_pivot_cols[1:] - _pivot_cols[:-1]) - 1
        idx = 0
        for r, c, e in zip(pivot_rows, pivot_cols, empty_rows):
            w = e * (r + 1)
            _data[0 : r + 1, c + 1 : c + 1 + e] = (
                params[idx : idx + w].reshape(e, r + 1).T
            )
            idx += w
    return _data


def rcef_pivot_rows(rcef_data: BinMat) -> IntVec:
    """
    Returns the pivot rows of the given binary matrix in RCEF.
    """
    n, m = rcef_data.shape
    num_pivot_rows = 0
    pivot_rows = np.zeros(m, dtype=np.int64)
    for c in range(m):
        pivot = pivot_idx(rcef_data[:, c], n)
        if pivot == n:
            break
        pivot_rows[c] = pivot
        num_pivot_rows += 1
    pivot_rows = pivot_rows[:num_pivot_rows]
    return pivot_rows


def rref_pivot_cols(rref_data: BinMat) -> IntVec:
    """
    Returns the pivot cols of the given binary matrix in RREF.
    """
    # return rcef_pivot_rows(rref_data.T)
    n, m = rref_data.shape
    num_pivot_cols = 0
    pivot_cols = np.zeros(n, dtype=np.int64)
    for r in range(n):
        pivot = pivot_idx(rref_data[r], m)
        if pivot == m:
            break
        pivot_cols[r] = pivot
        num_pivot_cols += 1
    pivot_cols = pivot_cols[:num_pivot_cols]
    return pivot_cols


def _rcef_params(
    rcef_data: BinMat, n: int, m: int, pivot_rows: IntVec, num_params: int
) -> BinVec:
    params = np.zeros(num_params, dtype=np.uint8)
    pivot_cols = np.arange(len(pivot_rows), dtype=np.uint8)
    _pivot_rows = np.hstack((pivot_rows, np.array([n], dtype=np.int64)))
    empty_cols = (_pivot_rows[1:] - _pivot_rows[:-1]) - 1
    idx = 0
    for r, c, e in zip(pivot_rows, pivot_cols, empty_cols):
        w = e * (c + 1)
        for j in range(e):
            _idx = idx + j * (c + 1)
            params[_idx : _idx + c + 1] = rcef_data[r + 1 + j, 0 : c + 1]
        idx += w
    return params


def _rref_params(
    rref_data: BinMat, n: int, m: int, pivot_cols: IntVec, num_params: int
) -> BinVec:
    # return _rcef_params(rref_data.T, m, n, pivot_cols, num_params)
    params = np.zeros(num_params, dtype=np.uint8)
    pivot_rows = np.arange(len(pivot_cols), dtype=np.uint8)
    _pivot_cols = np.hstack((pivot_cols, np.array([m], dtype=np.int64)))
    empty_rows = (_pivot_cols[1:] - _pivot_cols[:-1]) - 1
    idx = 0
    for r, c, e in zip(pivot_rows, pivot_cols, empty_rows):
        w = e * (r + 1)
        for j in range(e):
            _idx = idx + j * (r + 1)
            params[_idx : _idx + r + 1] = rref_data[0 : r + 1, c + 1 + j]
        idx += w
    return params


def get_rcef_args(rcef_data: BinMat) -> tuple[int, int, IntVec, BinVec]:
    """
    Given the binary data for a matrix in RCEF, returns the quadruple
    ``(n, m, pivot_rows, params)`` of the number ``n`` of rows, the number
    ``m`` of columns, the list ``pivot_rows`` of pivoc columns and the
    free binary parameters ``params`` for the RCEF matrix.
    """
    pivot_rows = rcef_pivot_rows(rcef_data)
    n, m = rcef_data.shape
    num_params = num_rcef_params(n, m, pivot_rows)
    params = _rcef_params(rcef_data, n, m, pivot_rows, num_params)
    return n, m, pivot_rows, params


def get_rref_args(rref_data: BinMat) -> tuple[int, int, IntVec, BinVec]:
    """
    Given the binary data for a matrix in RREF, returns the quadruple
    ``(n, m, pivot_cols, params)`` of the number ``n`` of rows, the number
    ``m`` of columns, the list ``pivot_cols`` of pivoc columns and the
    free binary parameters ``params`` for the RREF matrix.
    """
    # n, m, pivot_rows, params = get_rcef_args(rref_data.T)
    # return m, n, pivot_rows, params
    pivot_cols = rref_pivot_cols(rref_data)
    n, m = rref_data.shape
    num_params = num_rref_params(n, m, pivot_cols)
    params = _rref_params(rref_data, n, m, pivot_cols, num_params)
    return n, m, pivot_cols, params


def rcef_residual_vec(rcef_data: BinMat, vec: BinVec) -> BinVec:
    """
    Given the binary data for a matrix in RCEF and a vector ``vec`` with the
    same number of rows, returns the vector obtained by subtracting from ``vec``
    all those columns of the RCEF matrix which have their pivot at a row where
    ``vec`` takes the value ``1``.
    """
    n, m = rcef_data.shape
    vec = vec.copy()
    for c in range(m):
        col = rcef_data[:, c]
        pivot = pivot_idx(col, n)
        if vec[pivot]:
            vec ^= col
    return vec


def rref_residual_vec(rref_data: BinMat, vec: BinVec) -> BinVec:
    """
    Given the binary data for a matrix in RREF and a vector ``vec`` with the
    same number of cols, returns the vector obtained by subtracting from ``vec``
    all those rows of the RCEF matrix which have their pivot at a col where
    ``vec`` takes the value ``1``.
    """
    # return rcef_residual_vec(rref_data.T, vec)
    n, m = rref_data.shape
    vec = vec.copy()
    for r in range(n):
        row = rref_data[r]
        pivot = pivot_idx(row, m)
        if vec[pivot]:
            vec ^= row
    return vec


def bits_from_bytes(bytes_vec: UInt8Vec, n: int) -> BinVec:
    """
    Converts bytes to a binary vector containing the corresponding bits.
    The binary vector has length ``8*len(b)`` by default, containing all
    bits, but length can be truncated by specifying a desired ``num_bits``
    between ``len(b)-7`` and ``len(b)`` (both inclusive).
    If a length is specified, the bits ignored at the end must all be zero.
    """
    data_len = len(bytes_vec) * 8
    n = min(max(n, data_len - 7), data_len)
    data = np.zeros(data_len, dtype=np.uint8)
    for i in range(8):
        data[i::8] = np.where(bytes_vec & (2 ** (7 - i)), 1, 0)
    if data_len != n:
        data = data[:n].copy()
    return data


def bytes_from_bits(bit_vec: BinVec) -> UInt8Vec:
    """
    Compresses a binary vector into a vector of bytes.
    """
    num_bytes, r = divmod(len(bit_vec), 8)
    if r:
        num_bytes += 1
        bit_vec = np.append(bit_vec, np.zeros(8 - r, dtype=np.uint8))
    compressed_data = np.zeros(num_bytes, dtype=np.uint8)
    for i in range(8):
        compressed_data += 2 ** (7 - i) * bit_vec[i::8]
    return compressed_data


def matmul2(lhs: BinVecOrMat, rhs: BinVecOrMat) -> BinVecOrMat | Integral:
    """
    Multiplies two matrices/vectors.
    """
    return (lhs @ rhs) % 2  # type: ignore


def matmul_l2r(matrices: Sequence[BinMat]) -> BinMat:
    """
    Multiplies the given array of matrices, left-to-right.
    The sequence must be non-empty and the matrices must
    have compatible intermediate dimensions.

    .. warning::

        This function performs no validation of its input.
    """
    k = len(matrices)
    res = matrices[0].copy()
    for i in range(1, k):
        res @= matrices[i]
    return res % 2  # type: ignore


def matmul_r2l(matrices: Sequence[BinMat]) -> BinMat:
    """
    Multiplies the given array of matrices, right-to-left.
    The sequence must be non-empty and the matrices must
    have compatible intermediate dimensions.

    Same result as :func:`matmul_l2r`, but the sequence of
    matrix compositions is reversed.

    .. warning::

        This function performs no validation of its input.
    """
    k = len(matrices)
    res = matrices[-1]
    for i in range(k, -1, -1):
        res = matrices[i] @ res
    return res % 2  # type: ignore


def matmul_l2r_partial(
    start: BinVecOrMat, matrices: Sequence[BinMat]
) -> BinVecOrMat:
    """
    Multiples the given array of matrices, left-to-right, starting from the
    given ``start`` matrix (or row vector).
    The ``matrices`` must all be square, with dimension less than or equal
    to the number of columns in the ``start`` matrix.

    .. warning::

        This function performs no validation of its input.
    """
    start = start.copy()
    if len(start.shape) == 1:
        for m in matrices:
            n = m.shape[0]
            start[:n] = start[:n] @ m
    else:
        for m in matrices:
            n = m.shape[0]
            start[:, :n] = start[:, :n] @ m
    start %= 2
    return start


def matmul_r2l_partial(
    matrices: Sequence[BinMat], start: BinVecOrMat
) -> BinVecOrMat:
    """
    Multiples the given array of matrices, right-to-left, starting from the
    given ``start`` matrix (or col vector).
    The ``matrices`` must all be square, with dimension less than or equal
    to the number of rows in the ``start`` matrix.

    .. warning::

        This function performs no validation of its input.
    """
    start = start.copy()
    for m in matrices:
        n = m.shape[1]
        start[:n] = m @ start[:n]
    start %= 2
    return start


# For numba on Python 3.12,
# see: numba.discourse.group/t/ann-numba-0-59-0rc1-and-llvmlite-0-42-0rc1/2329
try:
    # If Numba is available, JIT compile all low-level functions:
    import numba  # type: ignore

    _FuncT = TypeVar("_FuncT")

    def _numba_compile(func: _FuncT) -> _FuncT:
        return numba.jit(nopython=True, cache=True)(func)  # type: ignore

    pivot_idx = _numba_compile(pivot_idx)

    rcef = _numba_compile(rcef)
    num_rcef_params = _numba_compile(num_rcef_params)
    make_rcef = _numba_compile(make_rcef)
    rcef_residual_vec = _numba_compile(rcef_residual_vec)
    rcef_pivot_rows = _numba_compile(rcef_pivot_rows)

    rref = _numba_compile(rref)
    num_rref_params = _numba_compile(num_rref_params)
    make_rref = _numba_compile(make_rref)
    rref_residual_vec = _numba_compile(rref_residual_vec)
    rref_pivot_cols = _numba_compile(rref_pivot_cols)

    bits_from_bytes = _numba_compile(bits_from_bytes)
    _rcef_params = _numba_compile(_rcef_params)
    _rcef_swap_pivot_col = _numba_compile(_rcef_swap_pivot_col)
    _rcef_clear_pivot_row = _numba_compile(_rcef_clear_pivot_row)
    _rref_params = _numba_compile(_rref_params)
    _rref_swap_pivot_row = _numba_compile(_rref_swap_pivot_row)
    _rref_clear_pivot_col = _numba_compile(_rref_clear_pivot_col)

    # No numba support for matmuls of integer types:
    # see: https://github.com/numba/numba/issues/6714
    # matmul = _numba_compile(matmul)
    # matapp_colvec = _numba_compile(matapp_colvec)
    # matapp_rowvec = _numba_compile(matapp_rowvec)

    # Only attempt to use Cupy if Numba is available,
    # see: https://github.com/numpy/numpy/issues/15973
    try:
        import cupy as cp  # type: ignore

        _matmul2 = matmul2

        def _gpu_matmul2(
            lhs: BinVecOrMat, rhs: BinVecOrMat
        ) -> BinVecOrMat | Integral:
            if not options.use_gpu:
                return _matmul2(lhs, rhs)
            lhs, rhs = cp.asarray(lhs), cp.asarray(rhs)
            return cp.asnumpy(_matmul2(lhs, rhs))  # type: ignore

        matmul2 = _gpu_matmul2

        _matmul_r2l = matmul_r2l

        def _gpu_matmul_r2l(matrices: Sequence[BinMat]) -> BinMat:
            if not options.use_gpu:
                return _matmul_r2l(matrices)
            matrices = [cp.asarray(m) for m in matrices]
            return cp.asnumpy(_matmul_r2l(matrices))  # type: ignore

        matmul_r2l = _gpu_matmul_r2l

        _matmul_l2r = matmul_l2r

        def _gpu_matmul_l2r(matrices: Sequence[BinMat]) -> BinMat:
            if not options.use_gpu:
                return _matmul_l2r(matrices)
            matrices = [cp.asarray(m) for m in matrices]
            return cp.asnumpy(_matmul_l2r(matrices))  # type: ignore

        matmul_l2r = _gpu_matmul_l2r

        _matmul_r2l_partial = matmul_r2l_partial

        def _gpu_matmul_r2l_partial(
            matrices: Sequence[BinMat], start: BinVecOrMat
        ) -> BinVecOrMat:
            if not options.use_gpu:
                return _matmul_r2l_partial(matrices, start)
            matrices = [cp.asarray(m) for m in matrices]
            start = cp.asarray(start)
            return cp.asnumpy(_matmul_r2l_partial(matrices, start))  # type: ignore

        matmul_r2l_partial = _gpu_matmul_r2l_partial

        _matmul_l2r_partial = matmul_l2r_partial

        def _gpu_matmul_l2r_partial(
            start: BinVecOrMat, matrices: Sequence[BinMat]
        ) -> BinVecOrMat:
            if not options.use_gpu:
                return _matmul_l2r_partial(start, matrices)
            start = cp.asarray(start)
            matrices = [cp.asarray(m) for m in matrices]
            return cp.asnumpy(_matmul_l2r_partial(start, matrices))  # type: ignore

        matmul_l2r_partial = _gpu_matmul_l2r_partial

    except ModuleNotFoundError:
        cp = None

except ModuleNotFoundError:
    numba = None
