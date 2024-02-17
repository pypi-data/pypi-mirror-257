"""
Generated affine partitions.
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
from abc import ABC, abstractmethod
from typing import Literal, final
from typing_extensions import Self
import numpy as np
from typing_validation import validate
from ..binalg import binvec, binmat, AffineSubspace
from .base import AP


class APMatrixGen(ABC):
    """
    Abstract base class for generators of invertible matrices, used to
    construct instances of :class:`~q1ss.ap.generated.GenAP`.
    """

    @staticmethod
    def eye(ambient_dim: int) -> EyeAPMatrixGen:
        """
        Generator of identity matrices.
        """
        return EyeAPMatrixGen(ambient_dim)

    @staticmethod
    def random(
        ambient_dim: int,
        *,
        seed: np.random.Generator | int | None = None,
    ) -> RandomAPMatrixGen:
        """
        Generator of random invertible matrices.
        """
        if not isinstance(seed, int):
            if isinstance(seed, np.random.Generator):
                rng = seed
            else:
                rng = np.random.default_rng(seed)
            seed = int(rng.integers(0, 1))
        return RandomAPMatrixGen(ambient_dim, seed)

    _ambient_dim: int
    _max_label_dim: int

    __slots__ = ("__weakref__", "_ambient_dim", "_max_label_dim")

    def __new__(
        cls, ambient_dim: int, max_label_dim: int | None = None
    ) -> Self:
        assert binvec.validate_dim(ambient_dim)
        if max_label_dim is None:
            max_label_dim = ambient_dim - 1
        else:
            assert binvec.validate_dim(max_label_dim, positive=False)
            max_label_dim = min(max_label_dim, ambient_dim - 1)
        instance = super().__new__(cls)
        instance._ambient_dim = ambient_dim
        instance._max_label_dim = max_label_dim
        return instance

    @property
    def ambient_dim(self) -> int:
        """
        The dimension of the ambient space for the generated matrices.
        """
        return self._ambient_dim

    @property
    def max_label_dim(self) -> int:
        """
        The maximum dimension of labels for which matrices can be generated.
        Maximum is :attr:`ambient_dim` minus 1.
        """
        return self._max_label_dim

    def __call__(self, label: binvec) -> tuple[binmat, binmat]:
        """
        Given a ``k``-dimensional label vector, returns the pair of a
        ``(n-k)``-dimensional matrix and its inverse, where ``n`` is the
        ambient dimension for the generator.

        :meta public:
        """
        assert self.__validate_label(label)
        n = self.ambient_dim
        k = len(label)
        mat, mat_inv = self._get_matrix(label)
        assert mat.shape == (n - k, n - k)
        return mat, mat_inv

    @abstractmethod
    def _get_matrix(self, label: binvec) -> tuple[binmat, binmat]:
        """
        Abstract method to be implemented by subclasses.

        Given a ``k``-dimensional label vector, returns the pair of a
        ``n-k``-dimensional matrix and its inverse, where ``n`` is the
        :attr:`~AP.ambient_dim` for the generator.

        The label vector has already been validated, and is guaranteed to have
        dimension between 0 and :attr:`~APMatrixGen.max_label_dim`,
        both inclusive.

        :meta public:
        """

    def __validate_label(self, label: binvec) -> Literal[True]:
        validate(label, binvec)
        if len(label) > self.max_label_dim:
            raise ValueError(
                f"Expected label of max dimension {self.max_label_dim}, "
                f"found {len(label)}."
            )
        return True


class EyeAPMatrixGen(APMatrixGen):
    """
    Generator of identity matrices.
    """

    def __new__(cls, ambient_dim: int) -> Self:
        """
        Constructs a generator of identity matrices with given ambient dim.

        :meta public:
        """
        return super().__new__(cls, ambient_dim)

    def __getnewargs__(self) -> tuple[int]:
        return (self.ambient_dim,)

    def _get_matrix(self, label: binvec) -> tuple[binmat, binmat]:
        """
        On a ``k``-dimensional label, returns a pair of ``(n-k)``-dimensional
        identity matrices, where ``n`` is the :attr:`~AP.ambient_dim`.

        :meta public:
        """
        m = binmat.eye(self.ambient_dim - len(label))
        return m, m


class RandomAPMatrixGen(APMatrixGen):
    """
    Generator of random invertible matrices.

    .. warning ::

        Currently, this is based on NumPy's pseudo-random generator:
        it is not possible to generate oracles for affine partitions
        based on this class of generators.

        In the future, an optional circuit property will be included in the
        :class:`APMatrixGen` class, allowing for the automatic generation of
        oracles for :class:`GenAP` instances.
        The functionality of this class will be extended to support
        circuit-defined pseudorandom functions, and NumPy's random number
        generator will be deprecated.

    """

    _seed: int

    __slots__ = ("_seed",)

    def __new__(cls, ambient_dim: int, seed: int) -> Self:
        """
        Constructs a generator of random invertible matrices with given ambient
        dimension and seed.

        :meta public:
        """
        instance = super().__new__(cls, ambient_dim)
        instance._seed = seed
        return instance

    @property
    def seed(self) -> int:
        """
        The seed used for generating random matrices.
        """
        return self._seed

    def __getnewargs__(self) -> tuple[int, int]:
        return (self.ambient_dim, self._seed)

    def _get_matrix(self, label: binvec) -> tuple[binmat, binmat]:
        """
        On a ``k``-dimensional label, returns the pair of a random
        ``(n-k)``-dimensional invertible matrix and its invers, where ``n``
        is the :attr:`~AP.ambient_dim`.

        The matrix and its inverse are sampled using :meth:`binmat.random_inv`,
        using a random number generator seeded by a combination of the label,
        the ambient dimension, and the :attr:`seed` provided.

        :meta public:
        """
        n, seed = self.ambient_dim, self._seed
        k = len(label)
        x = int(label) + (seed * n + k) * 2 ** (n - 1)
        rng = np.random.default_rng(x)
        return binmat.random_inv(n - k, rng=rng)


@final
class GenAP(AP):
    """
    Class for ordered balanced affine partitions of ``n``-bitstrings defined
    by a generator of invertible matrices for partial labels.
    """

    @staticmethod
    def random(
        subsp_dim: int,
        ambient_dim: int,
        *,
        seed: np.random.Generator | int | None = None,
    ) -> GenAP:
        """
        Creates random :class:`GenAP` for given subspace and ambient
        dimension, using :meth:`APMatrixGen.random` to create a random generator.
        """
        generator = APMatrixGen.random(ambient_dim, seed=seed)
        return GenAP(subsp_dim, generator)

    _generator: APMatrixGen

    __slots__ = ("_generator",)

    def __new__(cls, subsp_dim: int, generator: APMatrixGen) -> Self:
        """
        Constructs a new affine partition from the given labelled matrix
        generator.

        :meta public:
        """
        assert GenAP.__validate_data(subsp_dim, generator)
        instance = super().__new__(cls, subsp_dim, generator.ambient_dim)
        instance._generator = generator
        return instance

    def __getnewargs__(self) -> tuple[int, APMatrixGen]:
        """
        Method for pickling.
        """
        return (self.subsp_dim, self.generator)

    @property
    def generator(self) -> APMatrixGen:
        """
        The labelled matrix generator for this affine partition.
        """
        return self._generator

    def _get_subspace(self, label: binvec) -> AffineSubspace:
        r"""
        Returns the affine subspace corresponding to the given label,
        providing the underlying logic for :meth:`~AP.__getitem__`.

        Let ``k`` be the :attr:`~AP.label_dim` and ``n`` be the
        :attr:`~AP.ambient_dim` for this generator, so that ``n-k`` is the
        :attr:`~AP.subsp_dim`.

        1. Start from the standard affine subspace spanned by the first
           ``n-k`` standard basis vectors. The basepoint is given by a vector
           which is zero on the first ``n-k`` components, and is the reverse of
           the label on the remaining ``k`` components.
        2. Generate a sequence of ``k-1`` (matrix, inverse) pairs using partial
           labels, starting from ``label[:-1]`` and ending with the empty binary
           vector ``binvec([])``.
        3. Transform the standard subspace using the inverse matrices in the
           sequence, where matrix at index ``i`` acts on the subspace spanned
           by the first ``n-k+1+i`` std. basis vectors (``n-k+1`` -> ``n``).

        Uses the :meth:`AffineSubspace.transform` method with ``partial=True``.

        :meta public:
        """
        subsp_dim, ambient_dim = self.subsp_dim, self.ambient_dim
        basepoint = binvec.zeros(subsp_dim) | label[::-1]
        subsp = AffineSubspace.std(subsp_dim, ambient_dim, basepoint)
        matrices = [
            self.generator(label[:i])[1]  # select the inverse matrix
            for i in range(len(label) - 1, -1, -1)
        ]
        return subsp.transform(matrices, partial=True)

    def _label(self, vec: binvec) -> binvec:
        """
        Returns the label of the given vector in this affine partition,
        providing the underlying logic for :meth:`~AP.label`.

        Let ``k`` be the :attr:`~AP.label_dim` and ``n`` be the
        :attr:`~AP.ambient_dim` for this generator.

        1. Start from the given vector.
        2. For each ``i in range(k)``, generates a matrix using the last ``i``
           bits of the vector, read in reverse, then applies the matrix to the
           first ``n-i`` bits of the vector.
        3. Returns the last ``k`` bits of the resulting vector, read in reverse.

        Note that each matrix application keeps fixed the bits of the vector
        upon which the matrix itself depended.

        :meta public:
        """
        n, k, gen = self.ambient_dim, self.label_dim, self._generator
        vec = vec.copy()
        for i in range(k):
            mat, _ = gen(vec[-1 : -1 - i : -1])
            vec[: n - i] = mat @ vec[: n - i]
        return vec[-1 : -1 - k : -1]

    @staticmethod
    def __validate_data(
        subsp_dim: int, generator: APMatrixGen
    ) -> Literal[True]:
        validate(subsp_dim, int)
        validate(generator, APMatrixGen)
        min_subsp_dim = generator.ambient_dim - generator.max_label_dim
        if subsp_dim < min_subsp_dim:
            raise ValueError(
                f"Expected subspace dimension >= {min_subsp_dim}, "
                f"found {subsp_dim}."
            )
        return True
