# src/mesh/_core.py
r"""Core package functionality.

This module provides the :func:`mesh_file` function.

This function provides the toolkit's interface for meshing CAD files.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import time
import typing

from ._cadquery import cadquery_mesh_step
from ._config import config
from ._gmsh import gmsh_mesh_file


# ======================================================================
# CORE MESH FUNCTIONALITY
# ======================================================================


def mesh_file(
        in_file: pathlib.Path,
        *,
        mesh_engine: typing.Literal['cadquery', 'gmsh'] = 'cadquery',
        out_file: pathlib.Path | None = None
) -> pathlib.Path:
        r"""Mesh a CAD file to an output file.

        Args:
                in_file (`pathlib.Path`):
                        CAD file.
                mesh_engine (`typing.Literal['cadquery', 'gmsh']`):
                        Meshing engine(default: `'cadquery'`).
                out_file (`pathlib.Path | None`):
                        Output file (default: `None`).

        """

        if out_file is None:
                ts = time.strftime(r'%Y%m%d%H%M%S')
                out_file = config.work_dir / f'{ts}-mesh-{in_file.stem}.stl'

                if out_file.exists():
                        err = f"file already exists: '{out_file.as_posix()}'"
                        raise FileExistsError(err)

        match mesh_engine:
                case 'cadquery':
                        cadquery_mesh_step(in_file, out_file)
                case 'gmsh':
                        gmsh_mesh_file(in_file, out_file)
                case _:
                        err = f"invalid meshing engine '{mesh_engine}'"
                        raise ValueError(err)

        return out_file


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['mesh_file']


#<file:end>
