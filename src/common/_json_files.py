# src/common/_json_files.py
r"""JSON file structures.

This module provides the following types:

- :class:`CadQueryParamsJSON`
- :class:`GmshParamsJSON`

These types define the structure of JSON files used throughout the
project.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import typing

import cadquery

from ._pydantic import NonNegativeFloat


# ======================================================================
# CADQUERY PARAMETERS FILE
# ======================================================================


class CadQueryParamsJSON(typing.TypedDict):
        r"""CadQuery meshing parameters."""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        angular_tolerance: float  # TODO NonNegativeFloat?
        r"""Parameter `angularTolerance` in `cadquery.Workplane.export()`."""

        export_unit: cadquery.UnitLiterals
        r"""Parameter `outputUnit` in `cadquery.Workplane.export()`."""

        import_unit: cadquery.UnitLiterals
        r"""Parameter `unit` in `cadquery.importers.importStep()`."""

        internal_unit: cadquery.UnitLiterals
        r"""Parameter `unit` in `cadquery.Workplane.export()`."""

        opt_3mf: dict[str, typing.Any]
        r"""Parameter `opt` in `cadquery.Workplane.export()` for 3MF files."""

        opt_stl: dict[str, typing.Any]
        r"""Parameter `opt` in `cadquery.Workplane.export()` for STL files."""

        tolerance: float  # TODO NonNegativeFloat?
        r"""Parameter `tolerance` in `cadquery.Workplane.export()`."""


# ======================================================================
# GMSH PARAMETERS FILE
# ======================================================================


class GmshParamsJSON(typing.TypedDict):
        r"""Gmsh meshing parameters."""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        show_info: bool
        r"""Gmsh option 'General.Terminal'."""

        algorithm: typing.Literal[
                1,  # MeshAdapt
                2,  # Automatic
                3,  # Initial mesh only
                5,  # Delaunay
                6,  # Frontal-Delaunay
                7,  # BAMG
                8,  # Frontal-Delaunay for Quads
                9,  # Packing of Parallelograms
                11  # Quasi-structured Quad
        ]
        r"""Gmsh option 'Mesh.Algorithm'."""

        characteristic_length_min: NonNegativeFloat
        r"""Gmsh option 'Mesh.CharacteristicLengthMin'."""

        characteristic_length_max: NonNegativeFloat
        r"""Gmsh option 'Mesh.CharacteristicLengthMax'."""

        optimise: bool
        r""""Gmsh option 'Mesh.Optimise'."""


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'CadQueryParamsJSON',
        'GmshParamsJSON'
]


#<file:end>
