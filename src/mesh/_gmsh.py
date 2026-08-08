# src/mesh/_gmsh.py
r"""CAD file meshing using CadQuery.

This module provides the :func:`gmsh_mesh_file` function.

This function meshes a BREP, IGES, or STEP file to an STL file..

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib

import gmsh

from ._config import config
from src.common import GmshParamsJSON, load_json


# ======================================================================
# MESHING FUNCTION
# ======================================================================


def gmsh_mesh_file(
        in_file: pathlib.Path,
        out_file: pathlib.Path
) -> None:
        r"""Mesh a BREP, IGES, or STEP file to an STL file.

        Args:
                in_file (`pathlib.Path`):
                        CAD file.
                out_file (`pathlib.Path`):
                        Output file.

        """

        params_file = config.data_dir / 'mesh' / 'gmsh.json'

        params: GmshParamsJSON = load_json(params_file)

        gmsh.initialize()

        gmsh.option.setNumber('General.Terminal', params['show_info'])

        gmsh.model.add('part')
        gmsh.model.occ.importShapes(in_file.as_posix())

        gmsh.model.occ.synchronize()

        gmsh.option.setNumber('Mesh.MeshSizeFromCurvature', 0)
        gmsh.option.setNumber('Mesh.MeshSizeFromPoints', 0)
        gmsh.option.setNumber('Mesh.MeshSizeExtendFromBoundary', 0)

        gmsh.option.setNumber('Mesh.Algorithm', params['algorithm'])
        gmsh.option.setNumber(
                'Mesh.CharacteristicLengthMin',
                params['characteristic_length_min']
        )
        gmsh.option.setNumber(
                'Mesh.CharacteristicLengthMax',
                params['characteristic_length_max']
        )
        gmsh.option.setNumber('Mesh.Optimize', params['optimise'])

        gmsh.model.mesh.generate(2)
        gmsh.write(out_file.as_posix())

        gmsh.finalize()


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['gmsh_mesh_file']


#<file:end>
