# src/imgpy/models/_lenses.py
"""
TODO docstring for module _lenses

TODO:

- Add docstrings to all attributes.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import random
import typing

import pydantic

from src.common import PositiveFloat, StrictFrozenBase


# ======================================================================
# TODO TITLE
# ======================================================================


class LensSample(typing.NamedTuple):
        r"""TODO docstring for class 'LensSample'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        focal_length: PositiveFloat
        r"""TODO docstring"""

        f_stop: PositiveFloat
        r"""TODO docstring"""


# ======================================================================
# TODO TITLE
# ======================================================================


class PrimeLens(StrictFrozenBase):
        r"""TODO docstring for class 'PrimeLens'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        focal_length: PositiveFloat
        r"""Focal length of the lens."""

        f_stop_min: PositiveFloat
        r"""Minimum f-stop of the lens."""

        f_stop_max: PositiveFloat
        r"""Maximum f-stop of the lens."""


        # --------------------------------------------------------------
        # PUBLIC METHODS
        # --------------------------------------------------------------


        def sample(self) -> LensSample:
                r"""TODO docstring for method 'sample'"""

                f_stop = random.uniform(self.f_stop_min, self.f_stop_max)

                return LensSample(
                        focal_length=self.focal_length,
                        f_stop=f_stop
                )


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        @pydantic.model_validator(mode='after')
        def _validate_f_stops(self) -> typing.Self:
                r"""TODO docstring for method '_validate_f_stops'"""

                if self.f_stop_max < self.f_stop_min:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return self


class ZoomLens(StrictFrozenBase):
        r"""TODO docstring for class 'ZoomLens'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        focal_length_wide: PositiveFloat
        r"""Minimum focal length of the lens."""

        focal_length_tele: PositiveFloat
        r"""Maximum focal_length of the lens."""

        f_stop_wide_min: PositiveFloat
        r"""TODO docstring"""

        f_stop_wide_max: PositiveFloat
        r"""TODO docstring"""

        f_stop_tele_min: PositiveFloat
        r"""TODO docstring"""

        f_stop_tele_max: PositiveFloat
        r"""TODO docstring"""


        # --------------------------------------------------------------
        # PUBLIC METHODS
        # --------------------------------------------------------------


        def sample(self) -> LensSample:
                r"""TODO docstring for method 'sample'"""

                focal_length = random.uniform(
                                        self.focal_length_wide,
                                        self.focal_length_tele
                                )

                f_stop_max = (
                        (focal_length - self.focal_length_wide)
                        * (
                                (self.f_stop_tele_max - self.f_stop_wide_max)
                                / (
                                        self.focal_length_tele
                                        - self.focal_length_wide
                                )
                        )
                        + self.f_stop_wide_max
                )

                f_stop_min = (
                        (focal_length - self.focal_length_wide)
                        * (
                                (self.f_stop_tele_min - self.f_stop_wide_min)
                                / (
                                        self.focal_length_tele
                                        - self.focal_length_wide
                                )
                        )
                        + self.f_stop_wide_min
                )

                f_stop = random.uniform(f_stop_min, f_stop_max)

                return LensSample(focal_length=focal_length, f_stop=f_stop)


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        @pydantic.model_validator(mode='after')
        def _validate_focal_lengths(self) -> typing.Self:
                r"""TODO docstring for method '_validate_focal_lengths'"""

                if self.focal_length_tele <= self.focal_length_wide:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return self


        @pydantic.model_validator(mode='after')
        def _validate_f_stops(self) -> typing.Self:
                r"""TODO docstring for method '_validate_f_stops'"""

                if self.f_stop_tele_max < self.f_stop_tele_min:
                        err = f"TODO err msg"
                        raise ValueError(err)

                if self.f_stop_wide_max < self.f_stop_wide_min:
                        err = f"TODO err msg"
                        raise ValueError(err)

                return self


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'LensSample',
        'PrimeLens',
        'ZoomLens'
]


#<file:end>
