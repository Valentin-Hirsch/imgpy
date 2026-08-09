# src/post/_core.py
"""
Core package functionality.

This module provides the :func:`post_process` function.

This function provides the toolkit's interface for running post-
processing jobs.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import time

from ._config import config
from ._yolo import yolo
from .models import JobInput
from src.common import load_json


# ======================================================================
# POST PROCESSING
# ======================================================================


def post_process(
        input_file: pathlib.Path,
        *,
        out_dir: pathlib.Path | None = None
) -> pathlib.Path:
        r"""Run a post-processing job.

        Args:
                input_file (`pathlib.Path`):
                        Input file.
                out_dir (`pathlib.Path | None`):
                        Output directory (default: `None`).

        Returns:
                `pathlib.Path`:
                        Output directory.

        """

        job_input = JobInput(**load_json(input_file))

        if out_dir is None:
                ts = time.strftime(r'%Y%m%d-%H%M%S')

                out_dir = config.work_dir / f'{ts}-post-{job_input.job_name}'

                if out_dir.exists():
                        err = (
                                f"directory already exists: "
                                f"'{out_dir.as_posix()}'"
                        )
                        raise FileExistsError(err)

                out_dir.mkdir()

        in_dir = input_file.parent / job_input.directory

        match job_input.mode:
                case 'yolo_box':
                        yolo(in_dir, out_dir, job_input)
                case 'yolo_poly':
                        yolo(in_dir, out_dir, job_input)
                case _:
                        err = f"invalid mode: '{job_input.mode}'"
                        raise ValueError(err)

        return out_dir


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['post_process']


#<file:end>
