# src/imgpy/models/_jobinput.py
"""Rendering job input file model.

This module provides the :class:`JobInput` model.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import typing

import pydantic

from ._blender_objects import RigidBody
from ._lenses import PrimeLens, ZoomLens
from src.common import PositiveFloat, PositiveInt, StrictFrozenBase


# ======================================================================
# RENDERING JOB INPUT FILE MODEL
# ======================================================================


class JobInput(StrictFrozenBase):
        r"""Rendering job input file model."""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        class Protagonist(StrictFrozenBase):
                r"""TODO docstring for class 'Protagonist'"""


                # ------------------------------------------------------
                # ATTRIBUTES
                # ------------------------------------------------------

                additional_keys: dict[str, typing.Any]
                r"""TODO docstring"""

                file: pathlib.Path
                r"""TODO docstring"""

                name: str
                r"""TODO docstring"""

                rigid_body: RigidBody
                r"""TODO docstring"""


                # ------------------------------------------------------
                # INFRASTRUCTURE
                # ------------------------------------------------------


                @pydantic.field_validator('file', mode='before')
                @classmethod
                def _validate_file(cls, value: str) -> pathlib.Path:
                        r"""TODO docstring for method '_validate_file'"""

                        if isinstance(value, pathlib.Path):
                                return value
                        elif not isinstance(value, str):
                                err = f"TODO err msg"
                                raise ValueError(err)
                        else:
                                return pathlib.Path(value)


        class Render(StrictFrozenBase):
                r"""TODO docstring for class 'Render'"""


                # ------------------------------------------------------
                # INFRASTRUCTURE
                # ------------------------------------------------------


                class Resolution(StrictFrozenBase):
                        r"""TODO docstring for class 'Resolution'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        x: PositiveInt
                        r"""TODO docstring"""

                        y: PositiveInt
                        r"""TODO docstring"""


                # ------------------------------------------------------
                # ATTRIBUTES
                # ------------------------------------------------------

                additional_keys: dict[str, typing.Any]
                r"""TODO docstring"""

                device_type: typing.Literal['cpu', 'cuda', 'optix', 'hip']
                r"""TODO docstring"""

                file_format: typing.Literal['jpeg', 'png']
                r"""TODO docstring"""

                image_count: PositiveInt
                r"""TODO docstring"""

                resolution: Resolution
                r"""TODO docstring"""


        class Scene(StrictFrozenBase):
                r"""TODO docstring for class 'Scene'"""


                # ------------------------------------------------------
                # INFRASTRUCTURE
                # ------------------------------------------------------


                class ClutterObject(StrictFrozenBase):
                        r"""TODO docstring for class 'ClutterObject'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        count: PositiveInt
                        r"""TODO docstring"""

                        decimate_ratio: float = pydantic.Field(gt=0, le=1)
                        r"""TODO docstring"""

                        material: str
                        r"""TODO docstring"""

                        object: str
                        r"""TODO docstring"""

                        rigid_body: RigidBody
                        r"""TODO docstring"""

                        scale_factor: PositiveFloat
                        r"""TODO docstring"""

                        shade_mode: typing.Literal[
                                'smooth',
                                'auto_smooth',
                                'flat'
                        ]
                        r"""TODO docstring"""


                # ------------------------------------------------------
                # ATTRIBUTES
                # ------------------------------------------------------

                additional_keys: dict[str, typing.Any]
                r"""TODO docstring"""

                clutter: list[ClutterObject]
                r"""TODO docstring"""

                name: str
                r"""TODO docstring"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        job_name: str
        r"""Job name."""

        lens: PrimeLens | ZoomLens
        r"""Lens information."""

        protagonist: Protagonist
        r"""Protagonist information."""

        render: Render
        r"""Rendering information."""

        scene: Scene
        r"""Scene information."""


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['JobInput']


#<file:end>
