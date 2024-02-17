from __future__ import annotations
import numpy as np
import numpy.typing as npt
import pytest

import q1ss
from q1ss.binalg import binvec, binmat


def test_data() -> None:
    data = np.array([0, 1, 1, 0], dtype=np.uint8)
    v = binvec(data)
    assert v._data is data
    assert np.all(v.data == data)
    assert isinstance(v.data, np.ndarray)
    assert v._data.dtype == np.uint8


@pytest.mark.parametrize(
    "data",
    [
        [0, 1, 1, 0],
        np.array([0, 1, 1, 0]),
        np.array([0, 1, 1, 0], dtype=np.uint16),
    ],
)
def test_data_copy(data: npt.ArrayLike) -> None:
    v = binvec(data)
    assert v._data is not data
    assert np.all(v.data == data)


def test_readonly() -> None:
    data = np.array([0, 1, 1, 1], dtype=np.uint8)
    v = binvec(data, readonly=True)
    hash(v)
    with pytest.raises(TypeError):
        v.readonly = False
    with pytest.raises(binvec.ReadonlyError):
        v += v
    with pytest.raises(binvec.ReadonlyError):
        v *= v
    with pytest.raises(binvec.ReadonlyError):
        v @= binmat.eye(len(v))


def test_eq() -> None:
    assert binvec([0, 0]) != binvec([0, 1])
    assert binvec([0, 0]) != binvec([0, 0, 1])
    assert binvec([0, 1, 0]) == binvec([0, 1, 0])


def test_shape() -> None:
    v = binvec([0, 1, 0])
    assert v.shape == (3,)


def test_copy() -> None:
    v = binvec([0, 1, 0])
    w = v.copy()
    assert v is not w
    assert v._data is not w._data
    assert v == w


def test_arithmetic() -> None:
    v = binvec([0, 1, 0])
    w = binvec([1, 1, 0])
    assert +v == v
    assert -v == v
    assert v + w == binvec([1, 0, 0])
    assert v - w == v + w
    assert v * w == binvec([0, 1, 0])
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
    v = binvec.zeros(5)
    assert np.all(v._data == np.array([0, 0, 0, 0, 0], dtype=np.uint8))


def test_random() -> None:
    rng = np.random.default_rng(0)
    v = binvec.random(5, rng=rng)
    assert len(v) == 5


def test_el() -> None:
    matrix = np.array([binvec.el(j, 5)._data for j in range(5)], dtype=np.uint8)
    assert np.all(matrix == np.eye(5, dtype=np.uint8))


def test_iter_std_basis() -> None:
    matrix = np.array(
        [v._data for v in binvec.iter_std_basis(5)], dtype=np.uint8
    )
    assert np.all(matrix == np.eye(5, dtype=np.uint8))


def test_iter_all() -> None:
    matrix = np.array([v._data for v in binvec.iter_all(3)], dtype=np.uint8)
    assert np.all(
        matrix
        == np.array(
            [
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, 0],
                [0, 1, 1],
                [1, 0, 0],
                [1, 0, 1],
                [1, 1, 0],
                [1, 1, 1],
            ]
        )
    )


def test_from_bool() -> None:
    v = binvec.from_bool([True, False, [], 3])
    assert v == binvec([1, 0, 0, 1])


def test_from_str() -> None:
    v = binvec.from_str("1001")
    assert v == binvec([1, 0, 0, 1])


def test_bin() -> None:
    v_bin = "1010001011010110"
    v = binvec.from_str(v_bin)
    assert v.bin == v_bin


def test_hstack() -> None:
    v = binvec.hstack(
        [
            binvec([0, 1, 0]),
            binvec([1, 0]),
            binvec([1, 1, 0]),
        ]
    )
    assert v == binvec([0, 1, 0, 1, 0, 1, 1, 0])


def test_from_bytes() -> None:
    b = bytes([0b10100010, 0b11010110])
    assert np.all(binvec.from_bytes(b) == binvec.from_str("1010001011010110"))
    b = bytes([0b10100010, 0b11010000])
    assert np.all(binvec.from_bytes(b, 13) == binvec.from_str("1010001011010"))


def test_bytes() -> None:
    v = binvec.from_str("1010001011010110")
    assert bytes(v) == bytes([0b10100010, 0b11010110])
    v = binvec.from_str("1010001011010")
    assert bytes(v) == bytes([0b10100010, 0b11010000])


def test_getitem() -> None:
    v = binvec([1, 0, 0, 0, 1, 0])
    assert v[0] == 1
    assert v[-1] == 0
    assert v[1:3].is_zero
    assert v[-2:] == binvec([1, 0])


def test_setitem() -> None:
    v = binvec([0, 0, 0, 0, 0, 0])
    v[0] = 1
    assert v[0] == 1
    v[-1] = 1
    assert v[-1] == 1
    v[1:3] = 1
    assert all(b == 1 for b in v[1:3])
    v[-2:] = binvec([1, 0])
    assert v[-2:] == binvec([1, 0])


def test_or() -> None:
    v = binvec([1, 0, 1])
    w = binvec([0, 1, 0])
    assert v | w == binvec([1, 0, 1, 0, 1, 0])


def test_matmul() -> None:
    v = binvec([1, 0, 1])
    w = binvec([0, 1, 0])
    assert v @ v == 0
    assert w @ w == 1
    assert v @ w == 0


def test_len() -> None:
    v = binvec([1, 0, 1])
    assert len(v) == 3


def test_iter() -> None:
    v = binvec([1, 0, 1])
    assert list(v) == [1, 0, 1]


def test_data_error() -> None:
    with pytest.raises(ValueError):
        binvec([0, 1, 2])


def test_shape_error() -> None:

    v = binvec([0, 1, 0])
    w = binvec([1, 1])
    with pytest.raises(binvec.ShapeError):
        v + w
    with pytest.raises(binvec.ShapeError):
        v - w
    with pytest.raises(binvec.ShapeError):
        v * w
    with pytest.raises(binvec.ShapeError):
        v @ w


def test_int() -> None:
    v = binvec.from_str("0101101011")
    assert int(v) == 363
    rng = np.random.default_rng(0)
    for _ in range(5):
        v = binvec.random(10, rng=rng)
        assert int(v) == int(v.bin, 2)
        assert v == binvec.from_int(int(v), 10)
    assert binvec.from_int(0, 0) == binvec([])
