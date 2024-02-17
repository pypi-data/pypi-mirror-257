q1ss: Affine Partition Hashes
=================================

.. image:: https://img.shields.io/badge/python-3.10+-green.svg
    :target: https://docs.python.org/3.10/
    :alt: Python versions

.. image:: https://img.shields.io/pypi/v/aphash.svg
    :target: https://pypi.python.org/pypi/aphash/
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/status/aphash.svg
    :target: https://pypi.python.org/pypi/aphash/
    :alt: PyPI status

.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: https://github.com/python/mypy
    :alt: Checked with Mypy

.. image:: https://readthedocs.org/projects/aphash/badge/?version=latest
    :target: https://aphash.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square
    :target: https://github.com/RichardLitt/standard-readme
    :alt: standard-readme compliant


This library contains experimental implementations of quantum one-shot signatures by authors from the QSig Commission and other contributors, with special focus on blockchain technology.

.. contents::

Install
-------

The library is currently in pre-alpha development, but you can install the latest release from `PyPI <https://pypi.org/project/q1ss/>`_ as follows:

.. code-block:: console

    $ pip install --upgrade q1ss

Low-level operations are vectorised using `numpy <https://numpy.org/doc/stable/>`_, which is a required dependency of this library.

If `numba <https://numba.readthedocs.io/en/stable/>`_ is installed, it is automatically used to JIT-compile certain low-level operations for additional performance:

.. code-block:: console

    $ pip install --upgrade numba

If `cupy <https://docs.cupy.dev/en/stable/>`_ is installed additionally to `numba <https://numba.readthedocs.io/en/stable/>`_, GPU acceleration can be used for certain operations:

.. code-block:: console

    $ pip install --upgrade cupy


Usage
-----

Coming soon.


API
---

For the full API documentation, see https://q1ss.readthedocs.io/


License
-------

`LGPL © Hashberg Ltd and 20squares UG. <LICENSE>`_
