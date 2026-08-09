# src/imgpy/models/_locations.py
"""
TODO docstring for module _locations

TODO:

- Add docstrings to all attributes.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import random

from src.common import FrozenBase, StrictFrozenBase


# ======================================================================
# TODO TITLE
# ======================================================================


class Location(StrictFrozenBase):
        r"""TODO docstring for class 'Location'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        x: float
        r"""TODO"""

        y: float
        r"""TODO"""

        z: float
        r"""TODO"""



class LocationRange(FrozenBase):
        r"""TODO docstring for class 'LoactionRange'"""


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        x: tuple[float, float]
        r"""TODO"""

        y: tuple[float, float]
        r"""TODO"""

        z: tuple[float, float]
        r"""TODO"""


        # --------------------------------------------------------------
        # PUBLIC METHODS
        # --------------------------------------------------------------


        def sample(self) -> Location:
                r"""TODO docstring for method 'sample'"""

                return Location(
                        x=random.uniform(*self.x),
                        y=random.uniform(*self.y),
                        z=random.uniform(*self.z)
                )



# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'Location',
        'LocationRange'
]


#<file:end>
