# src/post/_config.py
"""
Package configuration.

This module provides the :data:`config` object.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib


# ======================================================================
# MESH CONFIG
# ======================================================================

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[2]


class _Config:
        r"""Container for package configuration options.

        This class stores configuration values used throughout the
        :mod:`post` package.

        """


        # --------------------------------------------------------------
        # DIRECTORIES
        # --------------------------------------------------------------

        data_dir: pathlib.Path = _PROJECT_ROOT / 'data'
        r"""Project data directory"""

        work_dir: pathlib.Path = _PROJECT_ROOT / 'workdir'
        r"""Project working directory"""


config = _Config()


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['config']


#<file:end>
