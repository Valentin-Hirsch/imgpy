# src/imgpy/blender/__init__.py
r"""Blender functionality package.

This package provides the following classes and functions:

- :class:`FileContext`
- :func:`apply_transforms`
- :func:`bake_simulation`
- :func:`import_material`
- :func:`import_node_tree`
- :func:`import_object`
- :func:`import_stl`
- :func:`render`
- :func:`set_origin`
- :func:`set_shading`
- :func:`set_up`

These symbols provide a robust interface to work with Blender.

"""


# ======================================================================
# IMPORTS
# ======================================================================

from ._common import render, set_up
from ._filecontext import FileContext
from ._utils import (
        apply_transforms,
        bake_simulation,
        import_material,
        import_node_tree,
        import_object,
        import_stl,
        set_origin,
        set_shading
)


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'render',
        'set_up',
        'FileContext',
        'apply_transforms',
        'bake_simulation',
        'import_material',
        'import_node_tree',
        'import_object',
        'import_stl',
        'set_origin',
        'set_shading'
]


#<file:end>
