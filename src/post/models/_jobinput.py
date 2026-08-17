# src/post/models/_jobinput.py
r"""Post-processing job input file model.

This module provides the :class:`JobInput` model.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import typing

from src.common import StrictFrozenBase


# ======================================================================
# POST-PROCESSING JOB INPUT FILE MODEL
# ======================================================================


class JobInput(StrictFrozenBase):
        r"""Post-processing job input file model."""

        additional_keys: dict[str, typing.Any]
        r"""Additional keys.

        Recognised keys:

        - `create_empty` (`bool`): write an empty label file for images
          with no annotated objects.
        - `min_component_area` (`int`): minimum pixel area of a
          connected mask component to be treated as a valid instance
          (filters out anti-aliasing noise at object borders).
        - `n_val` (`int`), `n_test` (`int`), `seed`: train/val/test
          split parameters.
        - `simplify` (`float`, `yolo_poly` only): polygon simplification
          factor passed to `cv2.approxPolyDP`.
        - `visualise` (`bool`): write visualisation images.

        """

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
