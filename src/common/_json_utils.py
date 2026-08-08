# src/common/_json_utils.py
r"""JSON utilities.

This module provides the following functions:

- :func:`load_json`
- :func:`save_json`

These functions provide a consistent interface for reading and writing
JSON files using the project's standard JSON and file handling
configuration.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import json
import pathlib
import typing


# ======================================================================
# FILE UTILITIES
# ======================================================================


def load_json(
        file: pathlib.Path,
        *, encoding: str = 'utf-8',
        **kwargs
) -> typing.Any:
        r"""Read and deserialise a JSON file.

        Args:
                file (`pathlib.Path`):
                        JSON file.
                encoding (`str`):
                        File encoding (default: `'utf-8'`).
                **kwargs (`typing.Any`):
                        Additional keyword arguments passed to
                        `json.load()`.

        Returns:
                `typing.Any`:
                        Read and deserialised JSON data.

        """

        with file.open(mode='r', encoding=encoding) as fp:
                        data = json.load(fp, **kwargs)

        return data


def save_json(
        obj: typing.Any,
        file: pathlib.Path,
        *,
        mode: str = 'x',
        encoding: str = 'utf-8',
        ensure_ascii: bool = False,
        indent: int = 4,
        sort_keys: bool = True,
        **kwargs: typing.Any
) -> None:
        r"""Serialise and save an object to a JSON file.

        Args:
                obj (`typing.Any`):
                        Object to serialise and save.
                file (`pathlib.Path`):
                        Output file.
                mode (`str`):
                        File access mode (default: `'x'`).
                encoding (`str`):
                        File encoding (default: `'utf-8'`).
                ensure_ascii (`bool`):
                        Argument passed to `json.dump()`
                        (default: `False`).
                indent (`int`):
                        Argument passed to `json.dump()` (default: `4`).
                sort_keys (`bool`):
                        Argument passed to `json.dump()`
                        (default: `True`).
                **kwargs (`typing.Any`):
                        Additional keyword arguments passed to
                        `json.dump()`.

        """

        with file.open(mode=mode, encoding=encoding) as fp:
                json.dump(
                        obj,
                        fp,
                        ensure_ascii=ensure_ascii,
                        indent=indent,
                        sort_keys=sort_keys,
                        **kwargs
                )


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'load_json',
        'save_json'
]


#<file:end>
