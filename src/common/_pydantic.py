# src/common/_pydantic.py
r"""Pydantic base classes and annotated types.

This module provides the following base classes:

- :class:`FrozenBase`
- :class:`StrictBase`
- :class:`StrictFrozenBase`

These classes implement the project's standard Pydantic configuration,
including strict validation, default value validation, and forbidden
extra fields.

This module also defines the following annotated types:

- :data:`PositiveInt`
- :data:`NonNegativeInt`
- :data:`PositiveFloat`
- :data:`NonNegativeFloat`

These types ... TODO

"""


# ======================================================================
# IMPORTS
# ======================================================================

import typing

import pydantic


# ======================================================================
# ANNOTATED TYPES
# ======================================================================

PositiveInt = typing.Annotated[int, pydantic.Field(gt=0)]
NonNegativeInt = typing.Annotated[int, pydantic.Field(ge=0)]

PositiveFloat = typing.Annotated[float, pydantic.Field(gt=0)]
NonNegativeFloat = typing.Annotated[float, pydantic.Field(ge=0)]


# ======================================================================
# BASE CLASSES
# ======================================================================


class FrozenBase(pydantic.BaseModel):
        r"""Base class for immutable Pydantic models."""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------

        model_config = pydantic.ConfigDict(
                extra='forbid',
                frozen=True,
                strict=False,
                validate_default=True
        )


class StrictBase(pydantic.BaseModel):
        r"""Base class for strict mutable Pydantic models."""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------

        model_config = pydantic.ConfigDict(
                extra='forbid',
                frozen=False,
                strict=True,
                validate_default=True
        )


class StrictFrozenBase(pydantic.BaseModel):
        r"""Base class for strict immutable Pydantic models."""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------

        model_config = pydantic.ConfigDict(
                extra='forbid',
                frozen=True,
                strict=True,
                validate_default=True
        )


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'PositiveInt',
        'NonNegativeInt',
        'PositiveFloat',
        'NonNegativeFloat',
        'FrozenBase',
        'StrictBase',
        'StrictFrozenBase'
]


#<file:end>
