from __future__ import annotations
from itertools import product
import numpy as np
import numpy.typing as npt
import pytest

import q1ss
from q1ss.binalg import binvec, binmat
from q1ss.binalg.vectorized import get_rcef_args, get_rref_args


def test_data() -> None:
    data = np.array([[0, 1], [1, 1]], dtype=np.uint8)
    v = binmat(data)
    assert v._data is data
    assert np.all(v.data == data)
    assert isinstance(v.data, np.ndarray)
    assert v._data.dtype == np.uint8


@pytest.mark.parametrize(
    "data",
    [
        [[0, 1], [1, 1]],
        np.array([[0, 1], [1, 1]]),
        np.array([[0, 1], [1, 1]], dtype=np.uint16),
    ],
)
def test_data_copy(data: npt.ArrayLike) -> None:
    v = binmat(data)
    assert v._data is not data
    assert np.all(v.data == data)


def test_readonly() -> None:
    data = np.array([[0, 1], [1, 1]], dtype=np.uint8)
    m = binmat(data, readonly=True)
    hash(m)
    with pytest.raises(TypeError):
        m.readonly = False
    with pytest.raises(binmat.ReadonlyError):
        m += m
    with pytest.raises(binmat.ReadonlyError):
        m *= m
    with pytest.raises(binmat.ReadonlyError):
        m @= m


def test_eq() -> None:
    assert binmat([[0, 1], [1, 1]]) != binmat([[0, 1], [1, 0]])
    assert binmat([[0, 1], [1, 1]]) != binmat([[0, 1]])
    assert binmat([[0, 1], [1, 1]]) == binmat([[0, 1], [1, 1]])


def test_shape() -> None:
    v = binmat([[0, 1], [1, 1], [1, 0]])
    assert v.shape == (3, 2)


def test_transpose() -> None:
    v = binmat([[0, 1], [1, 1], [1, 0]]).T
    assert v.shape == (2, 3)
    assert v == binmat([[0, 1, 1], [1, 1, 0]])


def test_copy() -> None:
    v = binmat([[0, 1], [1, 1], [1, 0]])
    w = v.copy()
    assert v is not w
    assert v._data is not w._data
    assert v == w


def test_arithmetic() -> None:
    v = binmat([[0, 1], [1, 1], [1, 0]])
    w = binmat([[1, 0], [0, 1], [1, 1]])
    assert +v == v
    assert -v == v
    assert v + w == binmat([[1, 1], [1, 0], [0, 1]])
    assert v - w == v + w
    assert v * w == binmat([[0, 0], [0, 1], [1, 0]])
    v2 = v.copy()
    v2 += w
    assert v2 == v + w
    v2 = v.copy()
    v2 -= w
    assert v2 == v - w
    v2 = v.copy()
    v2 *= w
    assert v2 == v * w


def test_zeros() -> None:
    v = binmat.zeros(3, 2)
    assert np.all(v._data == np.array([[0, 0], [0, 0], [0, 0]], dtype=np.uint8))


def test_random() -> None:
    rng = np.random.default_rng(0)
    v = binmat.random(2, 3, rng=rng)
    assert v.shape == (2, 3)


def test_eye() -> None:
    assert np.all(binmat.eye(5)._data == np.eye(5, dtype=np.uint8))


def test_from_rows() -> None:
    m = np.array([[1, 1], [1, 0], [0, 1]], dtype=np.uint8)
    assert binmat(m) == binmat.from_rows([binvec(row) for row in m])


def test_from_cols() -> None:
    m = np.array([[1, 1], [1, 0], [0, 1]], dtype=np.uint8)
    assert binmat(m) == binmat.from_cols([binvec(col) for col in m.T])


def test_vstack() -> None:
    u = binmat(
        [
            [0, 1],
            [0, 0],
        ]
    )
    v = binmat(
        [
            [1, 0],
        ]
    )
    w = binmat(
        [
            [1, 1],
            [0, 1],
            [1, 0],
        ]
    )
    m = binmat.vstack([u, v, w])
    res = binmat(
        [
            [0, 1],
            [0, 0],
            [1, 0],
            [1, 1],
            [0, 1],
            [1, 0],
        ]
    )
    assert m == res
    _v = binvec([1, 0])
    m = binmat.vstack([u, _v, w])
    assert m == res


def test_hstack() -> None:
    u = binmat(
        [
            [0],
            [1],
        ]
    )
    v = binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
        ]
    )
    w = binmat(
        [
            [1, 1],
            [1, 0],
        ]
    )
    m = binmat.hstack([u, v, w])
    res = binmat([[0, 1, 0, 1, 1, 1], [1, 0, 1, 1, 1, 0]])
    assert m == res
    _u = binvec([0, 1])
    m = binmat.hstack([_u, v, w])
    assert m == res


def test_block() -> None:
    blocks = [
        [binmat([[1]]), binmat([[0, 1]]), binmat([[1, 0]])],
        [
            binmat([[0], [0]]),
            binmat([[1, 0], [1, 1]]),
            binmat([[0, 0], [0, 1]]),
        ],
    ]
    res = binmat(
        [
            [1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1],
        ]
    )
    m = binmat.block(blocks)
    assert m == res


def test_block_diag() -> None:
    blocks = [
        binmat([[1]]),
        binmat([[1, 0], [1, 1]]),
        binmat([[0, 0], [1, 0]]),
    ]
    res = binmat(
        [
            [1, 0, 0, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0],
        ]
    )
    m = binmat.block_diag(blocks)
    assert m == res


def test_or() -> None:
    u = binmat(
        [
            [0],
            [1],
        ]
    )
    v = binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
        ]
    )
    m = u | v
    res = binmat([[0, 1, 0, 1], [1, 0, 1, 1]])
    assert m == res


@pytest.mark.parametrize("use_gpu", [False, True])
@pytest.mark.parametrize("inplace", [False, True])
def test_matmul(use_gpu: bool, inplace: bool) -> None:
    try:
        with q1ss.options(use_gpu=use_gpu):
            a = binmat(
                [
                    [1, 0],
                    [0, 1],
                    [0, 0],
                    [1, 1],
                ]
            )
            b = binmat(
                [
                    [1, 0, 1],
                    [0, 1, 1],
                ]
            )
            c = binmat(
                [
                    [1, 0, 1],
                    [0, 1, 1],
                    [0, 0, 0],
                    [1, 1, 0],
                ]
            )
            if inplace:
                a @= b
                assert a == c
            else:
                assert c == a @ b
    except ValueError:
        pass


@pytest.mark.parametrize("use_gpu", [False, True])
def test_matvmul(use_gpu: bool) -> None:
    try:
        with q1ss.options(use_gpu=use_gpu):
            a = binmat(
                [
                    [1, 0],
                    [0, 1],
                    [0, 0],
                    [1, 1],
                ]
            )
            b = binvec([1, 1])
            c = binvec([1, 1, 0, 0])
            assert c == a @ b
    except ValueError:
        pass


@pytest.mark.parametrize("use_gpu", [False, True])
@pytest.mark.parametrize("inplace", [False, True])
def test_vmatmul(use_gpu: bool, inplace: bool) -> None:
    try:
        with q1ss.options(use_gpu=use_gpu):
            a = binvec([1, 1])
            b = binmat(
                [
                    [1, 0, 1],
                    [0, 1, 1],
                ]
            )
            c = binvec([1, 1, 0])
            if inplace:
                a @= b
                assert c == a
            else:
                assert c == a @ b
    except ValueError:
        pass


def test_identity() -> None:
    a = binmat(
        [
            [1, 0],
            [0, 1],
            [0, 0],
            [1, 1],
        ]
    )
    assert not a.is_eye
    assert binmat.eye(5).is_eye


def test_getitem() -> None:
    a = binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    data = a._data
    n, m = a.shape
    for r in range(n):
        for c in range(m):
            assert a[r, c] == data[r, c]
    assert a[0] == binvec([1, 0, 1])
    assert a[0, :] == binvec([1, 0, 1])
    assert a[0, 1:] == binvec([0, 1])
    assert a[0, [2, 1]] == binvec([1, 0])
    assert a[:, 1] == binvec([0, 1, 0, 1])
    assert a[1::2, 1] == binvec([1, 1])
    assert a[[1, 2], 1] == binvec(
        [
            1,
            0,
        ]
    )
    assert a[:, :] == binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    assert a[1:, :] == binmat(
        [
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    assert a[1:3, :] == binmat(
        [
            [0, 1, 1],
            [0, 0, 0],
        ]
    )
    assert a[:, 1:] == binmat(
        [
            [0, 1],
            [1, 1],
            [0, 0],
            [1, 0],
        ]
    )
    assert a[:, 1:2] == binmat(
        [
            [0],
            [1],
            [0],
            [1],
        ]
    )
    assert a[1:, :2] == binmat(
        [
            [0, 1],
            [0, 0],
            [1, 1],
        ]
    )
    assert a[1:3, :2] == binmat(
        [
            [0, 1],
            [0, 0],
        ]
    )
    assert a[:3, 1:] == binmat(
        [
            [0, 1],
            [1, 1],
            [0, 0],
        ]
    )
    assert a[:3, 1:2] == binmat(
        [
            [0],
            [1],
            [0],
        ]
    )
    assert a[[1, 2, 3], :] == binmat(
        [
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    assert a[[1, 2], :] == binmat(
        [
            [0, 1, 1],
            [0, 0, 0],
        ]
    )
    assert a[:, [1, 2]] == binmat(
        [
            [0, 1],
            [1, 1],
            [0, 0],
            [1, 0],
        ]
    )
    assert a[:, [1]] == binmat(
        [
            [0],
            [1],
            [0],
            [1],
        ]
    )
    assert a[[1, 2, 3], [0, 1, 2]] == binvec([0, 0, 0])
    assert a[[0, 3, 2], [0, 1, 2]] == binvec([1, 1, 0])


def test_rank() -> None:
    a = binmat(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    assert a.rank == 0
    assert a.rcef == binmat(
        [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    assert a.T.rref == a.rcef.T
    assert a.T.rcef == a.rref.T
    a = binmat(
        [
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 1],
            [1, 0, 1],
        ]
    )
    assert a.rank == 1
    assert a.rcef == binmat(
        [
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
            [1, 0, 0],
        ]
    )
    assert a.T.rref == a.rcef.T
    assert a.T.rcef == a.rref.T
    a = binmat(
        [
            [1, 1, 1],
            [1, 1, 1],
            [0, 0, 0],
            [1, 1, 1],
        ]
    )
    assert a.rank == 1
    assert a.rcef == binmat(
        [
            [1, 0, 0],
            [1, 0, 0],
            [0, 0, 0],
            [1, 0, 0],
        ]
    )
    assert a.T.rref == a.rcef.T
    assert a.T.rcef == a.rref.T
    a = binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    assert a.rank == 2
    assert a.rcef == binmat(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [1, 1, 0],
        ]
    )
    assert a.T.rref == a.rcef.T
    assert a.T.rcef == a.rref.T
    a = binmat(
        [
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 0],
            [1, 1, 1],
        ]
    )
    assert a.rank == 3
    assert a.rcef == binmat(
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
            [0, 0, 1],
        ]
    )
    assert a.T.rref == a.rcef.T
    assert a.T.rcef == a.rref.T


def test_inverse() -> None:
    rng = np.random.default_rng(0)
    k = 10
    for _ in range(20):
        m = binmat.random(k, k, rng=rng)
        if m.rank == k:
            assert m.is_fullrank
            assert (m @ ~m).is_eye
            assert (~m @ m).is_eye


@pytest.mark.parametrize(
    "n, m",
    [
        (4, 6),
        (5, 5),
        (8, 4),
    ],
)
def test_ext_rcef(n: int, m: int) -> None:
    rng = np.random.default_rng(0)
    for _ in range(20):
        a = binmat.random(n, m, rng=rng)
        r, b = a.ext_rcef
        assert r.rank == a.rank
        assert b.rank == m
        assert r.shape == a.shape
        assert b.shape == (m, m)
        assert a @ b == r
        assert r @ ~b == a


@pytest.mark.parametrize(
    "n, m",
    [
        (4, 6),
        (5, 5),
        (8, 4),
    ],
)
def test_ext_rref(n: int, m: int) -> None:
    rng = np.random.default_rng(0)
    for _ in range(20):
        a = binmat.random(n, m, rng=rng)
        r, b = a.ext_rref
        assert r.rank == a.rank
        assert b.rank == n
        assert r.shape == a.shape
        assert b.shape == (n, n)
        assert b @ a == r
        assert ~b @ r == a


def test_random_inv() -> None:
    rng = np.random.default_rng(0)
    k = 10
    for _ in range(20):
        m, m_inv = binmat.random_inv(k, rng=rng)
        assert m.is_fullrank
        assert (m @ m_inv).is_eye
        assert (m_inv @ m).is_eye


def test_inv_rcef() -> None:
    rng = np.random.default_rng(0)
    k = 10
    for _ in range(20):
        m, m_inv = binmat.random_inv(k, rng=rng)
        assert m.rcef == binmat.eye(k)
        assert m_inv.rcef == binmat.eye(k)


def test_inv_rref() -> None:
    rng = np.random.default_rng(0)
    k = 10
    for _ in range(20):
        m, m_inv = binmat.random_inv(k, rng=rng)
        assert m.rref == binmat.eye(k)
        assert m_inv.rref == binmat.eye(k)


def test_rcef_matrix() -> None:
    for a, b, c, d in product([0, 1], repeat=4):
        res = binmat(
            [
                [1, 0, 0, 0],
                [a, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [b, c, d, 0],
                [0, 0, 0, 1],
            ]
        )
        n, m = res.shape
        pivot_rows = [0, 2, 3, 5]
        params = binvec([a, b, c, d])
        rcef_mat = binmat.rcef_matrix(n, m, pivot_rows, params)
        assert rcef_mat == res
    for a, b, c, d in product([0, 1], repeat=4):
        res = binmat(
            [
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [a, b, 0, 0, 0, 0],
                [c, d, 0, 0, 0, 0],
            ]
        )
        n, m = res.shape
        pivot_rows = [0, 1]
        params = binvec([a, b, c, d])
        rcef_mat = binmat.rcef_matrix(n, m, pivot_rows, params)
        assert rcef_mat == res


def test_rref_matrix() -> None:
    for a, b, c, d in product([0, 1], repeat=4):
        res = binmat(
            [
                [1, 0, 0, 0],
                [a, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [b, c, d, 0],
                [0, 0, 0, 1],
            ]
        ).T
        n, m = res.shape
        pivot_cols = [0, 2, 3, 5]
        params = binvec([a, b, c, d])
        rref_mat = binmat.rref_matrix(n, m, pivot_cols, params)
        assert rref_mat == res
    for a, b, c, d in product([0, 1], repeat=4):
        res = binmat(
            [
                [1, 0, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0],
                [a, b, 0, 0, 0, 0],
                [c, d, 0, 0, 0, 0],
            ]
        ).T
        n, m = res.shape
        pivot_cols = [0, 1]
        params = binvec([a, b, c, d])
        rref_mat = binmat.rref_matrix(n, m, pivot_cols, params)
        assert rref_mat == res


def test_id_rcef_matrix() -> None:
    assert binmat.rcef_matrix(5, 5, list(range(5))) == binmat.eye(5)


def test_id_rref_matrix() -> None:
    assert binmat.rref_matrix(5, 5, list(range(5))) == binmat.eye(5)


@pytest.mark.parametrize(
    "n, m",
    [
        (4, 6),
        (5, 5),
        (8, 4),
        (6, 4),
        (4, 8),
    ],
)
@pytest.mark.parametrize("rank", [2, 4, None])
def test_random_rcef(n: int, m: int, rank: int | None) -> None:
    rng = np.random.default_rng(0)
    for _ in range(20):
        a = binmat.random_rcef(n, m, rank, rng=rng)
        assert a.shape == (n, m)
        assert a.rank == (min(n, m) if rank is None else rank)
        assert a.rcef == a
        _n, _m, pivot_rows, params = get_rcef_args(a._data)
        assert (n, m) == (_n, _m)
        assert binmat.num_rcef_params(n, m, pivot_rows) == len(params)
        assert binmat.rcef_matrix(n, m, pivot_rows, params) == a


@pytest.mark.parametrize(
    "n, m",
    [
        (4, 6),
        (5, 5),
        (8, 4),
    ],
)
@pytest.mark.parametrize("rank", [2, 4, None])
def test_random_rref(n: int, m: int, rank: int | None) -> None:
    rng = np.random.default_rng(0)
    for _ in range(20):
        a = binmat.random_rref(n, m, rank, rng=rng)
        assert a.shape == (n, m)
        assert a.rank == (min(n, m) if rank is None else rank)
        assert a.rref == a
        _n, _m, pivot_rows, params = get_rref_args(a._data)
        assert (n, m) == (_n, _m)
        assert binmat.num_rref_params(n, m, pivot_rows) == len(params)
        assert binmat.rref_matrix(n, m, pivot_rows, params) == a


# @pytest.mark.parametrize("use_gpu", [False, True])
# def test_multiple_matmul_gpu(use_gpu: bool) -> None:
#     try:
#         with aphash.options(use_gpu=use_gpu):
#             rng = np.random.default_rng(0)
#             n = 10
#             for _ in range(10):
#                 matrices = [binmat.random(n, n, rng=rng) for _ in range(10)]
#                 res = binmat.matmul(matrices)
#                 exp_res = matrices[0].copy()
#                 for i in range(1, len(matrices)):
#                     exp_res @= matrices[i]
#                 assert res == exp_res
#     except ValueError:
#         return


# @pytest.mark.parametrize("use_gpu", [False, True])
# @pytest.mark.parametrize("rowvec", [False, True])
# def test_multiple_matapp_gpu(use_gpu: bool, rowvec: bool) -> None:
#     try:
#         with aphash.options(use_gpu=use_gpu):
#             rng = np.random.default_rng(0)
#             n = 10
#             for _ in range(10):
#                 vec = binvec.random(n, rng=rng)
#                 matrices = [binmat.random(n, n, rng=rng) for _ in range(10)]
#                 if rowvec:
#                     res = binmat.matapp(vec, matrices)
#                 else:
#                     res = binmat.matapp(matrices, vec)
#                 exp_res = vec.copy()
#                 if rowvec:
#                     for m in matrices:
#                         exp_res @= m
#                 else:
#                     for m in matrices[::-1]:
#                         exp_res = m @ exp_res
#                 assert res == exp_res
#     except ValueError:
#         return


def test_rows() -> None:
    a = binmat(
        [
            [1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1],
        ]
    )
    assert len(a.rows) == a.shape[0]
    assert list(a.rows) == [
        binvec([1, 0, 1, 1, 0]),
        binvec([0, 1, 0, 0, 0]),
        binvec([0, 1, 1, 0, 1]),
    ]
    for i, row in enumerate(a._data):
        assert a.rows[i] == binvec(row)
    assert a.rows[:2] == binmat(
        [
            [1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
        ]
    )
    assert a.rows[[0, 2]] == binmat(
        [
            [1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1],
        ]
    )


def test_cols() -> None:
    a = binmat(
        [
            [1, 0, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1],
        ]
    )
    assert len(a.cols) == a.shape[1]
    assert list(a.cols) == [
        binvec([1, 0, 0]),
        binvec([0, 1, 1]),
        binvec([1, 0, 1]),
        binvec([1, 0, 0]),
        binvec([0, 0, 1]),
    ]
    for i, col in enumerate(a._data.T):
        assert a.cols[i] == binvec(col)
    assert a.cols[1:3] == binmat(
        [
            [0, 1],
            [1, 0],
            [1, 1],
        ]
    )
    assert a.cols[[2, 1, 4]] == binmat(
        [
            [1, 0, 0],
            [0, 1, 0],
            [1, 1, 1],
        ]
    )
