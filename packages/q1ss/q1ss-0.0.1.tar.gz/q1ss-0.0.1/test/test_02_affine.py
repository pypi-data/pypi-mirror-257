from __future__ import annotations
from itertools import product
import numpy as np
import pytest
from q1ss.binalg import binvec, binmat, AffineSubspace


def test_data() -> None:
    generators = binmat(
        [
            [1, 0, 1, 0],  # <- generator 1
            [1, 1, 1, 1],  # <- generator 2
            [0, 0, 1, 1],  # <- generator 3
        ]
    )  # <- transpose so generators become cols
    basepoint = binvec([0, 0, 0, 1])
    subsp = AffineSubspace(generators, basepoint)
    assert subsp.generators == generators
    assert subsp.basepoint == basepoint
    assert subsp.ambient_dim == 4
    assert not subsp.is_canonical


def test_canonicalize() -> None:
    generators = binmat([[1, 0, 1, 0], [1, 1, 1, 1], [0, 0, 1, 1]])
    basis = binmat(
        [
            [1, 0, 0, 1],  # <- basis vector 1
            [0, 1, 0, 1],  # <- basis vector 2
            [0, 0, 1, 1],  # <- basis vector 3
        ]
    )  # <- transpose so generators become cols
    basepoint = binvec([0, 0, 0, 1])
    subsp = AffineSubspace(generators, basepoint)
    subsp.canonicalize()
    assert subsp.is_canonical
    assert subsp.basis == basis
    assert subsp.basepoint == basepoint
    assert not subsp.is_linear
    assert list(subsp.iter_basis) == list(basis)


def test_eq() -> None:
    generators = binmat([[1, 0, 1, 0], [1, 1, 1, 1], [0, 0, 1, 1]])
    basepoint = binvec([0, 0, 0, 1])
    subsp = AffineSubspace(generators, basepoint)
    canon_subsp = subsp.copy(canonical=True)
    assert subsp == canon_subsp
    assert subsp.is_canonical


@pytest.mark.parametrize(
    "ambient_dim, num_generators", [(5, 2), (6, 4), (10, 4), (10, 10)]
)
def test_canonicalize_random(ambient_dim: int, num_generators: int) -> None:
    rng = np.random.default_rng(0)
    for _ in range(10):
        generators = binmat.random(num_generators, ambient_dim, rng=rng)
        basepoint = binvec.random(ambient_dim, rng=rng)
        basis = generators.rref
        basis = basis[: basis.rank]
        subsp = AffineSubspace(generators, basepoint)
        subsp.canonicalize()
        assert subsp.is_canonical
        assert subsp.basis == basis
        for basis_vec in subsp.iter_basis:
            pivot = next(idx for idx, b in enumerate(basis_vec) if b)
            assert subsp.basepoint[pivot] == 0, (pivot, subsp.basepoint)


def test_is_disjoint() -> None:
    subspaces = [
        AffineSubspace(binmat([[1, 0, 0]]), binvec([0, 0, 1])),
        AffineSubspace(binmat([[1, 1, 0]]), binvec([0, 0, 0])),
        AffineSubspace(binmat([[1, 0, 1]]), binvec([0, 1, 0])),
        AffineSubspace(binmat([[1, 1, 1]]), binvec([1, 0, 0])),
    ]
    for subsp1, subsp2 in product(subspaces, repeat=2):
        if subsp1 is not subsp2:
            assert subsp1.is_disjoint(subsp2)


def test_is_linear() -> None:
    assert not AffineSubspace(binmat([[1, 0, 0]]), binvec([0, 0, 1])).is_linear
    assert AffineSubspace(binmat([[1, 1, 0]]), binvec([0, 0, 0])).is_linear


def test_points() -> None:
    basis = binmat([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    basepoint = binvec([0, 0, 0, 1])
    subsp = AffineSubspace(basis, basepoint)
    points = subsp.points
    assert points.shape == (8, 4)
    assert points == binmat(
        [
            [0, 0, 0, 1],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 1, 1],
            [1, 1, 0, 1],
            [1, 1, 1, 0],
        ]
    )
    assert list(points) == list(subsp.iter_points)


def test_residual() -> None:
    basis = binmat([[1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]])
    basepoint = binvec([0, 0, 0, 1])
    subsp = AffineSubspace(basis, basepoint)
    for point in subsp.iter_points:
        assert subsp.residual(point).is_zero
        assert point in subsp
    v = binvec([1, 1, 1, 1])
    assert subsp.residual(v) == binvec([0, 0, 0, 1])


@pytest.mark.parametrize(
    "ambient_dim, subsp_dim", [(5, 2), (6, 4), (10, 4), (10, 10)]
)
@pytest.mark.parametrize("linear", [False, True])
def test_random_subsp(subsp_dim: int, ambient_dim: int, linear: bool) -> None:
    rng = np.random.default_rng(0)
    for _ in range(5):
        subsp = AffineSubspace.random(
            subsp_dim, ambient_dim, linear=linear, rng=rng
        )
        assert subsp.ambient_dim == ambient_dim
        assert subsp.dim == subsp_dim
        if linear:
            assert subsp.is_linear


@pytest.mark.parametrize(
    "ambient_dim, subsp_dim", [(5, 2), (6, 4), (10, 4), (10, 10)]
)
@pytest.mark.parametrize("linear", [False, True])
def test_random_points(subsp_dim: int, ambient_dim: int, linear: bool) -> None:
    rng = np.random.default_rng(0)
    for _ in range(5):
        subsp = AffineSubspace.random(
            subsp_dim, ambient_dim, linear=linear, rng=rng
        )
        for _ in range(5):
            points = subsp.random_points(20, rng=rng)
            for point in points:
                assert point in subsp


@pytest.mark.parametrize(
    "ambient_dim, subsp_dim", [(5, 2), (6, 4), (10, 4), (10, 10)]
)
@pytest.mark.parametrize("linear", [False, True])
def test_subsp_transl(subsp_dim: int, ambient_dim: int, linear: bool) -> None:
    rng = np.random.default_rng(0)
    for _ in range(5):
        subsp = AffineSubspace.random(
            subsp_dim, ambient_dim, linear=linear, rng=rng
        )
        for _ in range(10):
            shift = binvec.random(ambient_dim, rng=rng)
            shifted_subsp = subsp + shift
            assert subsp.basepoint + shift in shifted_subsp
            if shift not in subsp.linspace:
                assert shifted_subsp.is_disjoint(subsp)


@pytest.mark.parametrize(
    "ambient_dim, subsp_dim", [(5, 2), (6, 4), (10, 4), (10, 10)]
)
@pytest.mark.parametrize("linear", [False, True])
def test_subsp_transform(
    subsp_dim: int, ambient_dim: int, linear: bool
) -> None:

    rng = np.random.default_rng(0)
    for _ in range(5):
        subsp = AffineSubspace.random(
            subsp_dim, ambient_dim, linear=linear, rng=rng
        )
        points = subsp.points
        for _ in range(10):
            ambient_dim_delta = rng.integers(-3, +4)
            new_ambient_dim = ambient_dim + int(ambient_dim_delta)
            mat = binmat.random(new_ambient_dim, ambient_dim, rng=rng)
            transformed_subsp = mat @ subsp
            for point in points:
                assert mat @ point in transformed_subsp


# TODO: test iterated transforms
# TODO: test is_ortho
