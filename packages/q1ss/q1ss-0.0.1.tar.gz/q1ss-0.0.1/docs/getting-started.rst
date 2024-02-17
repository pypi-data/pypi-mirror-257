Getting Started
===============

This library contains experimental implementations of quantum one-shot signatures by authors from the QSig Commission. It is in pre-alpha development, but you can install the latest release from `PyPI <https://pypi.org/project/q1ss/>`_ as follows:

.. code-block:: console

    $ pip install --upgrade q1ss

Low-level operations are vectorised using `numpy <https://numpy.org/doc/stable/>`_, which is a required dependency of this library.

If `numba <https://numba.readthedocs.io/en/stable/>`_ is installed, it is automatically used to JIT-compile certain low-level operations for additional performance:

.. code-block:: console

    $ pip install --upgrade numba

If `cupy <https://docs.cupy.dev/en/stable/>`_ is installed additionally to `numba <https://numba.readthedocs.io/en/stable/>`_, GPU acceleration can be used for certain operations:

.. code-block:: console

    $ pip install --upgrade cupy

Unlike JIT compilation, which is automatically performed when `numba <https://numba.readthedocs.io/en/stable/>`_ is detected, GPU acceleration is opt-in: it can be enabled by setting the :attr:`~q1ss.utils.options.Q1SSOptions.use_gpu` attribute of the global library :obj:`~q1ss.utils.options.options` to :obj:``True``.

GitHub repo: https://github.com/The-QSig-Commission/q1ss
