# src/imgpy/protocols/_scene.py
r"""TODO docstring for module _scene

This module provides the following types:

- :class:`SetUpFunction`
- :class:`RandomiseFunction`
- :class:`Scene`

TODO

TODO:

- Add docstrings for all attributes.

"""


# ======================================================================
# IMPORTS
# ======================================================================

from __future__ import annotations

import typing

from ..models import JobInput
from src.common import StrictFrozenBase

from typing import TYPE_CHECKING
if TYPE_CHECKING:
        from ..blender import FileContext


# ======================================================================
# TODO TITLE
# ======================================================================


class SetUpFunction(typing.Protocol):
        r"""TODO docstring for class 'SetUpFunction'"""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        def __call__(
                self,
                *,
                job_input: JobInput,
                scene_config: StrictFrozenBase,
                fctx: FileContext
        ) -> None:
                r"""TODO docstring for function '__call__'"""

                ...


class RandomiseFunction(typing.Protocol):
        r"""TODO docstring for class 'RandomiseFunction'"""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        def __call__(
                self,
                *,
                job_input: JobInput,
                scene_config: StrictFrozenBase,
                image_nr: int,
                fctx: FileContext
        ) -> None:
                r"""TODO docstring for function '__call__'"""

                ...


class Scene(typing.NamedTuple):
        r"""TODO docstring for class 'Scene'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        Config: type[StrictFrozenBase]

        set_up: SetUpFunction
        randomise: RandomiseFunction


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'SetUpFunction',
        'RandomiseFunction',
        'Scene'
]


#<file:end>
