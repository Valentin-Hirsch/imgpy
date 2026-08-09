# src/post/models/_jobinput.py
r"""Post-processing job input file model.

This module provides the :class:`JobInput` model.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import typing

from src.common import NonNegativeInt, StrictFrozenBase


# ======================================================================
# POST-PROCESSING JOB INPUT FILE MODEL
# ======================================================================


class JobInput(StrictFrozenBase):
        r"""Post-processing job input file model."""

        additional_keys: dict[str, typing.Any]
        r"""Additional keys."""

        class_id: NonNegativeInt
        r"""Protagonist class id."""

        directory: pathlib.Path
        r"""Input image directory"""

        file_format: typing.Literal['jpeg', 'png']
        r"""Input images file format."""

        job_name: str
        r"""Job name."""

        mode: typing.Literal['yolo_box', 'yolo_poly']
        r"""Psot-processing mode."""



# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['JobInput']


#<file:end>
