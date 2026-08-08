# src/common/__init__.py
r"""Project-wide utilities, types, and structures.

This package provides the following symbols:

**JSON file sturctures:**

- :class:`CadQueryParamsJSON`
- :class:`GmshParamsJSON`
- :class:`RunInputFileJSON`
- :class:`PostInputFileJSON`

**Pydantic base classes:**

- :class:`FrozenBase`
- :class:`StrictBase`
- :class:`StrictFrozenBase`

**Pydantic annotated types:**

- :data:`PositiveInt`
- :data:`NonNegativeInt`
- :data:`PositiveFloat`
- :data:`NonNegativeFloat`

**Utilities:**

- :func:`load_json`
- :func:`save_json`

"""


# ======================================================================
# IMPORTS
# ======================================================================

from ._json_files import (
        CadQueryParamsJSON,
        GmshParamsJSON,
        PostInputFileJSON,
        RenderInputFileJSON
)
from ._json_utils import load_json, save_json
from ._pydantic import (
        FrozenBase,
        NonNegativeFloat,
        NonNegativeInt,
        PositiveFloat,
        PositiveInt,
        StrictBase,
        StrictFrozenBase
)


# ======================================================================
# PACKAGE EXPORT
# ======================================================================

__all__ = [
        'CadQueryParamsJSON',
        'GmshParamsJSON',
        'RenderInputFileJSON',
        'PostInputFileJSON',
        'load_json',
        'save_json',
        'FrozenBase',
        'PositiveInt',
        'NonNegativeInt',
        'PositiveFloat',
        'NonNegativeFloat',
        'StrictBase',
        'StrictFrozenBase'
]


#<file:end>
