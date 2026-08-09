# src/post/__init__.py
r"""Image post-processing package

This package provides the following symbols:

- :data:`config`
- :func:`post_process`

These symbols provide the interface for running post-processing jobs.

"""


# ======================================================================
# IMPORTS
# ======================================================================

from ._config import config
from ._core import post_process


# ======================================================================
# PACKAGE EXPORT
# ======================================================================

__all__ = [
        'config',
        'post_process'
]


#<file:end>
