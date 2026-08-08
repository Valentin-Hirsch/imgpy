# src/common/_json_files.py
r"""JSON file structures.

This module provides the following types:

- :class:`RenderInputFileJSON`
- :class:`PostInputFileJSON`
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
# RUN INPUT FILE
# ======================================================================


class RenderInputFileJSON(typing.TypedDict):
        r"""Rendering job input file."""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        # TODO


# ======================================================================
# POST INPUT FILE
# ======================================================================


class PostInputFileJSON(typing.TypedDict):
        r"""Post-processing job input file."""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        # TODO


# ======================================================================
# CADQUERY PARAMETERS FILE
# ======================================================================


class _CadQueryOptJSON(typing.TypedDict):
        r"""Additional CadQuery meshing parameters."""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        ascii: bool
        r"""Parameter `ascii` in `cadquery.Shape.exportStl()` via `opt`."""

        parallel: bool
        r"""Parameter `parallel` in `cadquery.Shape.exportStl()` via `opt`."""

        relative: bool
        r"""Parameter `relative` in `cadquery.Shape.exportStl()` via `opt`."""


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
        'RenderInputFileJSON',
        'PostInputFileJSON',
        'CadQueryParamsJSON',
        'GmshParamsJSON'
]


#<file:end>
