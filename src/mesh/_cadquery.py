# src/mesh/_cadquery.py
r"""CAD file meshing using CadQuery.

This module provides the :func:`cadquery_mesh_step` function.

This function meshes a STEP file to an output file..

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib

import cadquery

from ._config import config
from src.common import CadQueryParamsJSON, load_json


# ======================================================================
# MESHING FUNCTION
# ======================================================================


def cadquery_mesh_step(
        in_file: pathlib.Path,
        out_file: pathlib.Path,
) -> None:
        r"""Mesh a STEP file to an output file.

        Args:
                in_file (`pathlib.Path`):
                        CAD file.
                out_file (`pathlib.Path`):
                        Output file.

        """

        params_file = config.data_dir / 'mesh' / 'cadquery.json'

        params: CadQueryParamsJSON = load_json(params_file)
        opt_params = params[f'opt_{out_file.suffix[1:].lower()}']

        part = cadquery.importers.importStep(
                in_file.as_posix(),
                params['import_unit']
        )

        part.export(
                out_file.as_posix(),
                tolerance=params['tolerance'],
                angularTolerance=params['angular_tolerance'],
                unit=params['internal_unit'],
                outputUnit=params['export_unit'],
                opt=opt_params
        )


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['cadquery_mesh_step']


#<file:end>
