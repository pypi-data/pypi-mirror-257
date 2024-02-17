from __future__ import annotations
import numpy as np
import pytest
from q1ss.binalg import binvec, binmat, AffineSubspace
from q1ss.ap import GenAP, SeqAP, ExplicitAP


def test_explicit() -> None:
    subspaces = [
        AffineSubspace(binmat([[1, 0, 0]]), binvec([0, 0, 1])),
        AffineSubspace(binmat([[1, 1, 0]]), binvec([0, 0, 0])),
        AffineSubspace(binmat([[1, 0, 1]]), binvec([0, 1, 0])),
        AffineSubspace(binmat([[1, 1, 1]]), binvec([1, 0, 0])),
    ]
    partition = ExplicitAP(subspaces)
    assert partition.ambient_dim == 3
    assert partition.subsp_dim == 1
    assert partition.label_dim == 2
    assert len(partition) == 4
    assert list(partition) == subspaces
    for i, subsp in enumerate(subspaces):
        assert partition[i] is subsp
    for v, subsp in zip(binvec.iter_all(2), subspaces):
        assert partition[v] is subsp
        for point in subsp.points:
            assert partition.label(point) == v


def test_random_explicit_ap() -> None:
    rng = np.random.default_rng(0)
    for _ in range(10):
        ambient_dim = rng.integers(3, 6, dtype=int)
        subsp_dim = rng.integers(1, ambient_dim + 1, dtype=int)
        partition = ExplicitAP.random(subsp_dim, ambient_dim, rng=rng)
        assert len(partition) == len(partition._subspaces)
        partition.validate()


def test_random_generated_ap() -> None:
    rng = np.random.default_rng(0)
    for _ in range(10):
        ambient_dim = rng.integers(3, 6, dtype=int)
        subsp_dim = rng.integers(1, ambient_dim + 1, dtype=int)
        partition = GenAP.random(subsp_dim, ambient_dim, seed=rng)
        partition.validate()
        assert partition == partition.explicit


def test_random_sequence_ap() -> None:
    rng = np.random.default_rng(0)
    for _ in range(10):
        ambient_dim = rng.integers(3, 6, dtype=int)
        subsp_dim = rng.integers(1, ambient_dim + 1, dtype=int)
        partition = SeqAP.random(subsp_dim, ambient_dim, rng=rng)
        partition.validate()
        assert partition == partition.explicit
        assert partition == partition.as_generated
