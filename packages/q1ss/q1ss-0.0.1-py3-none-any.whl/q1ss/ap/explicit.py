"""
Explicitly specified affine partitions.
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
from collections.abc import Iterator, Sequence
from typing import Literal, final
from typing_extensions import Self
import numpy as np
from typing_validation import validate
from ..binalg import binvec, AffineSubspace
from .base import AP


@final
class ExplicitAP(AP):
    """
    Class for ordered balanced affine partitions of ``n``-bitstrings explicitly
    specified by a complete family of disjoint affine subspaces.
    """

    @staticmethod
    def random(
        subsp_dim: int,
        ambient_dim: int,
        *,
        rng: np.random.Generator | int | None = None,
    ) -> ExplicitAP:
        """
        Samples a random affine partition with given subspace and ambient
        dimensions.

        Sampling random affine partitions is an expensive operation
        in general, and the running time grows exponentially with
        the ambient dimension.

        .. warning::

            This method relies on
            :meth:`~q1ss.binalg.affine.AffineSubspace.random` to sample
            subspaces, which does not result in a uniform distribution over
            affine partitions.
            This will change in future releases.

        .. warning::

            The current implementation of this method is by rejection sampling,
            so it can be very slow even for small number of affine subspaces.
            This will change in future releases.

        """
        assert AffineSubspace._validate_dimensions(subsp_dim, ambient_dim)
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        num_subspaces = 2 ** (ambient_dim - subsp_dim)
        subspaces: list[AffineSubspace] = []
        for _ in range(num_subspaces):
            subsp = AffineSubspace.random(subsp_dim, ambient_dim, rng=rng)
            while not all(subsp.is_disjoint(other) for other in subspaces):
                subsp = AffineSubspace.random(subsp_dim, ambient_dim, rng=rng)
            subspaces.append(subsp)
        return ExplicitAP(subspaces)

    _subspaces: tuple[AffineSubspace, ...]

    __slots__ = ("_subspaces",)

    def __new__(cls, subspaces: Sequence[AffineSubspace]) -> Self:
        """
        Creates a new explicit affine partition from the given
        sequence of disjoint affine subspaces.

        :meta public:
        """
        assert ExplicitAP.__validate_subspaces(subspaces)
        _subsp = subspaces[0]
        instance = super().__new__(cls, _subsp.dim, _subsp.ambient_dim)
        instance._subspaces = tuple(subspaces)
        return instance

    def __getnewargs__(self) -> tuple[Sequence[AffineSubspace]]:
        """
        Method for pickling.
        """
        return (self._subspaces,)

    def _get_subspace(self, label: binvec) -> AffineSubspace:
        """
        Returns the affine subspace corresponding to the given label,
        providing the underlying logic for :meth:`~AP.__getitem__`.

        The desired subspace is accessed from internal memory and returned.

        :meta public:
        """
        assert self.__validate_label(label)
        return self._subspaces[int(label)]

    def __iter__(self) -> Iterator[AffineSubspace]:
        """
        A more efficient iterator over the subspaces.
        """
        return iter(self._subspaces)

    @staticmethod
    def __validate_subspaces(
        subspaces: Sequence[AffineSubspace],
    ) -> Literal[True]:
        validate(subspaces, Sequence[AffineSubspace])
        if not subspaces:
            raise ValueError("Expected at least one affine subspace.")
        _subsp = subspaces[0]
        dim, ambient_dim = _subsp.dim, _subsp.ambient_dim
        for subsp in subspaces:
            if subsp.dim != dim:
                raise ValueError(
                    "All affine subspaces must have equal dimension: "
                    f"expected {dim}, found {subsp.dim}."
                )
            if subsp.ambient_dim != ambient_dim:
                raise ValueError(
                    "All affine subspaces must have equal ambient dimension: "
                    f"expected {ambient_dim}, found {subsp.ambient_dim}."
                )
        label_dim = ambient_dim - dim
        if len(subspaces) != 2**label_dim:
            raise ValueError(
                f"Expected 2^{label_dim} affine subspaces, "
                f"found {len(subspaces)}."
            )
        for i, subsp_i in enumerate(subspaces):
            for j in range(i + 1, len(subspaces)):
                subsp_j = subspaces[j]
                if not subsp_i.is_disjoint(subsp_j):
                    raise ValueError(
                        f"Affine subspaces at indexes {i} and {j} intersect."
                    )
        return True

    def __validate_label(self, label: binvec) -> Literal[True]:
        validate(label, binvec)
        if len(label) != self.label_dim:
            raise ValueError(
                f"Expected label of dimension {self.label_dim}, "
                f"found {len(label)}."
            )
        return True
