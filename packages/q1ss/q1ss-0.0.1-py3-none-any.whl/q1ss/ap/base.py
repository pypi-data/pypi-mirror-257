"""
Abstract base class for ordered affine partitions.
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
from collections.abc import Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Any, Literal
from typing_extensions import Self
import numpy as np
from typing_validation import validate
from ..binalg import binvec, AffineSubspace
from ..binalg.affine import BinvecLabelFun, HypercubeAxes


if TYPE_CHECKING:
    from .explicit import ExplicitAP


class AP(ABC):
    """
    Abstract base class for ordered balanced affine partitions
    of ``n``-bitstrings.
    """

    _subsp_dim: int
    _ambient_dim: int
    _label_dim: int

    __slots__ = ("__weakref__", "_subsp_dim", "_ambient_dim", "_label_dim")

    def __new__(cls, subsp_dim: int, ambient_dim: int) -> Self:
        assert AffineSubspace._validate_dimensions(subsp_dim, ambient_dim)
        instance = super().__new__(cls)
        instance._subsp_dim = subsp_dim
        instance._ambient_dim = ambient_dim
        instance._label_dim = ambient_dim - subsp_dim
        return instance

    @property
    def subsp_dim(self) -> int:
        """
        The dimension of the affine subspaces in the partition.
        """
        return self._subsp_dim

    @property
    def ambient_dim(self) -> int:
        """
        The dimension of the ambient space.
        """
        return self._ambient_dim

    @property
    def label_dim(self) -> int:
        """
        The dimension of the label vectors for subspaces in this partition
        """
        return self._label_dim

    @property
    def explicit(self) -> ExplicitAP:
        """
        Returns an explicit representation of this affine partition.
        """
        from .explicit import ExplicitAP

        return ExplicitAP(list(self))

    def validate(
        self,
        *,
        num_vecs: int | None = None,
        num_labels: int | None = None,
        rng: np.random.Generator | int | None = None,
    ) -> None:
        """
        Validates the partition:

        - checks that all subspaces have the correct dimensions
        - checks that all pairs of distinct subspaces are disjoint
        - checks that all vectors belong to the subspace with associated label
        - checks that orthogonality relationships are correct

        If ``num_vecs`` and ``num_labels`` are not specified, the method will
        validate the partition using all possible vectors and labels,
        respectively. Otherwise, it will use the specified number of random
        vectors and labels.
        """
        ambient_dim, subsp_dim = self.ambient_dim, self.subsp_dim
        label_dim = self.label_dim
        if not isinstance(rng, np.random.Generator):
            rng = np.random.default_rng(rng)
        # 1. Lists of vectors and labels to be used for validation:
        if num_vecs is None:
            vecs = list(binvec.iter_all(ambient_dim))
            num_vecs = len(vecs)
        else:
            vecs = [
                binvec.random(ambient_dim, rng=rng) for _ in range(num_vecs)
            ]
        if num_labels is None:
            labels = list(binvec.iter_all(label_dim))
            num_labels = len(labels)
        else:
            labels = [
                binvec.random(label_dim, rng=rng) for _ in range(num_vecs)
            ]
        # 2. Check that all subspaces have the correct dimensions:
        for label in labels:
            subsp = self[label]
            if subsp.ambient_dim != ambient_dim:
                raise ValueError(
                    f"Expected ambient dimension {ambient_dim}, "
                    f"found {subsp.ambient_dim}."
                    f"\nSubspace label: {label}"
                )
            if subsp.dim != subsp_dim:
                raise ValueError(
                    f"Expected subspace dimension {subsp_dim}, "
                    f"found {subsp.dim}."
                    f"\nSubspace label: {label}"
                )
        # 3. Check that all pairs of distinct subspaces are disjoint:
        for i, label_i in enumerate(labels):
            subsp_i = self[label_i]
            for j in range(i + 1, num_labels):
                subsp_j = self[labels[j]]
                if not subsp_i.is_disjoint(subsp_j):
                    raise ValueError(
                        "Subspaces are not disjoint."
                        f"\nLHS subspace label: {label_i}"
                        f"\nRHS subspace label: {labels[j]}"
                    )
        # 4. Check that all labels are correct:
        for vec in vecs:
            label = self.label(vec)
            if vec not in self[label]:
                raise ValueError(
                    "Vector is not in the subspace for its assigned label."
                    f"\nVector: {vec}"
                    f"\nLabel: {label}"
                )
        # 5. Check that orthogonality relationships are correct:
        for vec in vecs:
            for label in labels:
                exp_res = self[label].is_ortho(vec)
                res = self.is_ortho(vec, label)
                if res != exp_res:
                    exp_descr = "orthogonal" if exp_res else "not orthogonal"
                    descr = "orthogonal" if res else "not orthogonal"
                    raise ValueError(
                        "Orthogonality relationship is incorrect."
                        f"Expected {exp_descr}, found {descr}."
                        f"\nVector: {vec}"
                        f"\nLabel: {label}"
                    )

    def label(self, vec: binvec) -> binvec:
        """
        Returns the label of the given vector in this affine partition.
        """
        assert self.__validate_ambient_vector(vec)
        return self._label(vec)

    def is_ortho(self, vec: binvec, label: binvec) -> bool:
        """
        Returns whether the given vector is orthogonal to the affine subspace
        corresponding to the given label in this affine partition
        """
        assert self.__validate_ambient_vector(vec)
        assert self.__validate_label(label)
        return self._is_ortho(vec, label)

    def draw(
        self,
        axes: HypercubeAxes,
        *,
        colors: Sequence[str] | None = None,
        label: BinvecLabelFun | None = None,
        subsp_kwargs: Sequence[Mapping[str, Any]] | None = None,
        **draw_networkx_kwargs: Any,
    ) -> None:
        """
        Draws the affine partition using :func:`~networkx.draw_networkx`.
        """
        AffineSubspace.draw_many(
            axes,
            list(self),
            colors=colors,
            label=label,
            subsp_kwargs=subsp_kwargs,
            **draw_networkx_kwargs,
        )

    def __len__(self) -> int:
        """
        The number of subspaces in this partition.

        :meta public:
        """
        return int(2 ** (self.label_dim))

    def __iter__(self) -> Iterator[AffineSubspace]:
        """
        Iterates over the subspaces in this partition.

        :meta public:
        """
        label_dim = self.label_dim
        for idx in range(2**label_dim):
            yield self[binvec.from_int(idx, label_dim)]

    def __getitem__(self, label: binvec | int) -> AffineSubspace:
        """
        Returns the affine subspace corresponding to the given label
        in this affine partition.

        :meta public:
        """
        if isinstance(label, int):
            label = binvec.from_int(label, self.label_dim)
        assert self.__validate_label(label)
        return self._get_subspace(label)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AP):
            return NotImplemented
        if self.ambient_dim != other.ambient_dim:
            return False
        if self.subsp_dim != other.subsp_dim:
            return False
        return all(s == t for s, t in zip(self, other))

    @abstractmethod
    def _get_subspace(self, label: binvec) -> AffineSubspace:
        """
        Abstract method to be implemented by subclasses,
        providing the underlying logic for :meth:`__getitem__`.

        Returns the affine subspace corresponding to the given label.
        The label vector has already been validated, and is guaranteed to have
        dimension equal to the :attr:`label_dim` for the partition.

        :meta public:
        """

    def _label(self, vec: binvec) -> binvec:
        """
        Returns the label of the given vector in this affine partition,
        providing the underlying logic for :meth:`~AP.label`.

        The default implementation works by brute force search over all
        affine subspaces: subclasses can override this method to provide
        a more efficient implementation.

        :meta public:
        """
        for idx, subsp in enumerate(self):
            if vec in subsp:
                return binvec.from_int(idx, self.label_dim)
        assert False, f"Vector {vec} should be in one of the subspaces."

    def _is_ortho(self, vec: binvec, label: binvec) -> bool:
        """
        Returns whether the given vector is orthogonal to the affine subspace
        corresponding to the given label in this affine partition,
        providing the underlying logic for :meth:`AP.is_ortho`.

        The default implementation relies on producing the affine subspace and
        explicitly testing for orthogonality:  subclasses can override this
        method to provide a more efficient implementation.

        :meta public:
        """
        return self[label].is_ortho(vec)

    def __validate_label(self, label: binvec) -> Literal[True]:
        validate(label, binvec)
        if len(label) != self.label_dim:
            raise ValueError(
                f"Expected label of dimension {self.label_dim}, "
                f"found {len(label)}."
            )
        return True

    def __validate_ambient_vector(self, vec: binvec) -> Literal[True]:
        validate(vec, binvec)
        if len(vec) != self.ambient_dim:
            raise ValueError(
                f"Expected vector of dimension {self.ambient_dim}, "
                f"found {len(vec)}."
            )
        return True
