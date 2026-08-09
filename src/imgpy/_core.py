# src/imgpy/_core.py
r"""Core package functionality.

This module provides the function :func:`render_images`.

This function provides the toolkit's interface for running image
rendering jobs.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import importlib.util
import pathlib
import shutil
import time

import bpy

from ._config import config
from .blender import render, set_up
from .models import JobInput
from .protocols import Scene
from src.common import load_json


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def _import_scene(file: pathlib.Path) -> Scene:
        r"""Import an ImgPy scene.

        TODO

        Args:
                file (`pathlib.Path`):
                        TODO

        Returns:
                `Scene`:
                        TODO

        """

        spec = importlib.util.spec_from_file_location(file.stem, file)

        if spec is None:
                err = (
                        f"could not create module spec for file "
                        f"'{file.as_posix()}'"
                )
                raise RuntimeError(err)  # TODO exc type

        if spec.loader is None:
                err = (
                        f"module spec has no loader for file "
                        f"'{file.as_posix()}'"
                )
                raise RuntimeError(err)  # TODO exc type

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        Config = getattr(module, 'SceneConfig')
        set_up = getattr(module, 'set_up')
        randomise = getattr(module, 'randomise')

        # TODO validate class and functions

        return Scene(Config=Config, set_up=set_up, randomise=randomise)


# ======================================================================
# IMAGE RENDERING
# ======================================================================


def render_images(
        input_file: pathlib.Path,
        *,
        job_dir: pathlib.Path | None = None,
) -> pathlib.Path:
        r"""Run an image rendering job.

        Args:
                input_file (`pathlib.Path`):
                        Input file.
                job_dir (`pathlib.Path | None`):
                        Job directory (default: `None`).

        Returns:
                `pathlib.Path`:
                        Job directory

        """

        job_input = JobInput(**load_json(input_file))

        if job_dir is None:
                ts = time.strftime(r'%Y%m%d-%H%M%S')

                job_dir = config.work_dir / f'{ts}-render-{job_input.job_name}'

                if job_dir.exists():
                        err = (
                                f"directory already exists: "
                                f"'{job_dir.as_posix()}'"
                        )
                        raise FileExistsError(err)

                job_dir.mkdir()


        # TODO from here

        scene_name = job_input.scene.name
        scene_dir = config.data_dir / 'blender' / 'scenes' / scene_name

        scene = _import_scene(scene_dir / f'{scene_name}.py')
        scene_config = scene.Config(
                **load_json(scene_dir / f'{scene_name}.json')
        )

        blend_file = job_dir / 'main.blend'
        shutil.copy(scene_dir / f'{scene_name}.blend', blend_file)

        bpy.ops.wm.open_mainfile(filepath=blend_file.as_posix())

        fctx = set_up(job_input, input_file.parent)

        scene.set_up(job_input=job_input, scene_config=scene_config, fctx=fctx)

        bpy.ops.wm.save_mainfile()



        for i in range(job_input.render.image_count):
                scene.randomise(
                        job_input=job_input,
                        scene_config=scene_config,
                        image_nr=i,
                        fctx=fctx
                )

                render(f'{i}', fctx)

        bpy.ops.wm.save_mainfile()

        return job_dir


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['render_images']


#<file:end>
