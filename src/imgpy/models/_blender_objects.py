# src/imgpy/models/_blender_objects.py
"""
TODO docstring for module _blender_objects

TODO:

- Add docstrings for all attributes.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import typing

import pydantic

from ._locations import LocationRange
from src.common import (
        FrozenBase,
        NonNegativeFloat,
        PositiveFloat,
        StrictFrozenBase
)



# ======================================================================
# TODO TITLE
# ======================================================================


class AreaLight(FrozenBase):
        r"""TODO docstring for class 'AreaLight'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        location_range: LocationRange
        r"""TODO"""

        power_range: tuple[NonNegativeFloat, NonNegativeFloat]
        r"""TODO"""

        temperature_range: tuple[NonNegativeFloat, NonNegativeFloat]
        r"""TODO"""



        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        @pydantic.field_validator('power_range')
        @classmethod
        def _todo_name_1(
                cls,
                value: tuple[NonNegativeFloat, NonNegativeFloat]
        ) -> tuple[NonNegativeFloat, NonNegativeFloat]:
                r"""TODO docstring for method '_todo_name_1'"""

                if value[1] < value[0]:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return value


        @pydantic.field_validator('temperature_range')
        @classmethod
        def _todo_name_2(
                cls,
                value: tuple[NonNegativeFloat, NonNegativeFloat]
        ) -> tuple[NonNegativeFloat, NonNegativeFloat]:
                r"""TODO docstring for method '_todo_name_2'"""

                if value[1] < value[0]:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return value


class SpotLight(FrozenBase):
        r"""TODO docstring for class 'SpotLight'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        location_range: LocationRange
        r"""TODO"""

        power_range: tuple[NonNegativeFloat, NonNegativeFloat]
        r"""TODO"""

        temperature_range: tuple[NonNegativeFloat, NonNegativeFloat]
        r"""TODO"""



        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        @pydantic.field_validator('power_range')
        @classmethod
        def _todo_name_1(
                cls,
                value: tuple[NonNegativeFloat, NonNegativeFloat]
        ) -> tuple[NonNegativeFloat, NonNegativeFloat]:
                r"""TODO docstring for method '_todo_name_1'"""

                if value[1] < value[0]:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return value


        @pydantic.field_validator('temperature_range')
        @classmethod
        def _todo_name_2(
                cls,
                value: tuple[NonNegativeFloat, NonNegativeFloat]
        ) -> tuple[NonNegativeFloat, NonNegativeFloat]:
                r"""TODO docstring for method '_todo_name_2'"""

                if value[1] < value[0]:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return value


# ======================================================================
# TODO TITLE
# ======================================================================


class RigidBody(StrictFrozenBase):
        r"""TODO docstring for class '_RigidBody'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        collision_shape: typing.Literal['convex_hull', 'mesh']
        r"""TODO"""

        friction: float = pydantic.Field(gt=0, le=1)  # TODO are these limits correct
        r"""TODO"""

        mass: PositiveFloat
        r"""TODO"""

        restitution: float = pydantic.Field(gt=0, le=1)  # TODO are these limits correct
        r"""TODO"""



# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'AreaLight',
        'SpotLight',
        'RigidBody'
]


#<file:end>
