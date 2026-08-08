# src/mesh/__init__.py
r"""CAD file meshing package.

This package provides the following symbols:

- :data:`config`
- :data:`MESH_ENGINES`
- :func:`mesh_file`

These symbols provide the interface for meshing CAD files.

"""


# ======================================================================
# IMPORTS
# ======================================================================

from ._config import config
from ._constants import MESH_ENGINES
from ._core import mesh_file


# ======================================================================
# PACKAGE EXPORT
# ======================================================================

__all__ = [
        'config',
        'MESH_ENGINES',
        'mesh_file'
]


#<file:end>
