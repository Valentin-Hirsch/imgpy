# src/imgpy/protocols/_cycles.py
r"""TODO docstring for module _cycles

This module provides the following protocols:

- :class:`CyclesPreferences`
- :class:`CyclesSettings`

TODO

TODO:

- Add docstrings for all attributes.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import typing


# ======================================================================
# TODO TITLE
# ======================================================================


class CyclesPreferences(typing.Protocol):
        r"""TODO docstring for class 'CyclesPreferences'"""


        # ==============================================================
        # ATTRIBUTES
        # ==============================================================

        compute_device_type: str


        # ==============================================================
        # PUBLIC METHODS
        # ==============================================================


        def refresh_devices(
                self,
                *args: typing.Any,
                **kwargs: typing.Any
        ) -> typing.Any:
                r"""TODO docstring for method 'refresh_devices'"""

                ...


class CyclesSettings(typing.Protocol):
        r"""TODO docstring for class 'CyclesSettings'"""


        # ==============================================================
        # ATTRIBUTES
        # ==============================================================

        device: str


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'CyclesPreferences',
        'CyclesSettings'
]


#<file:end>
