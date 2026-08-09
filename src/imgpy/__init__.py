# src/imgpy/__init__.py
r"""Image rendering package.

This package provides the following symbols:

- :data:`config`
- :func:`render_images`

These symbols provide the interface for running rendering jobs.

"""


# ======================================================================
# IMPORTS
# ======================================================================

from ._config import config
from ._core import render_images


# ======================================================================
# PACKAGE EXPORT
# ======================================================================

__all__ = [
        'config',
        'render_images'
]


#<file:end>
