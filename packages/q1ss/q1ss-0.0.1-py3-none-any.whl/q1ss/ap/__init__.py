"""
Implementation of Affine Partition functions, ased on
`eprint.iacr.org/2020/107 <https://eprint.iacr.org/2020/107>`_ and work by
the authors of the :mod:`q1ss` library.

Classes in this module:

- :class:`AP` is the abstract base class for all affine partition functions.
- :class:`ExplicitAP` is a concrete implementation based on an explicit
    specification of the affine partition, as a complete collection of
    disjoint :class:`~q1ss.binalg.affine.AffineSubspace` instances.
- :class:`GenAP` is a concrete implementation based on pluggable logic
    which generates invertible matrices based on partial label vectors.
- :class:`SeqAP` is a concrete implementation based on fixed sequences
    of invertible matrices.

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

from .base import AP
from .explicit import ExplicitAP
from .generated import GenAP, APMatrixGen
from .sequence import SeqAP, SeqAPData

__all__ = (
    "AP",
    "ExplicitAP",
    "GenAP",
    "APMatrixGen",
    "SeqAP",
    "SeqAPData",
)
