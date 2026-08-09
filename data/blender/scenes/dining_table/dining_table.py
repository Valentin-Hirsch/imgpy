# TODO description
r"""TODO docstring

TODO

"""


# ======================================================================
# IMPORTS
# ======================================================================

import math
import random
import typing

import mathutils  # pyright: ignore[reportMissingModuleSource]  # TODO fix
import pydantic

from src.common import PositiveInt, StrictFrozenBase
from src.imgpy.blender import FileContext, bake_simulation
from src.imgpy.models import (
        AreaLight,
        JobInput,
        Location,
        LocationRange,
        SpotLight
)


# ======================================================================
# TODO TITLE
# ======================================================================


class SceneConfig(StrictFrozenBase):
        r"""TODO docstring for class 'SceneConfig'"""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------


        class Render(StrictFrozenBase):
                r"""TODO docstring for class 'Render'"""


                # ------------------------------------------------------
                # INFRASTRUCTURE
                # ------------------------------------------------------


                class Camera(StrictFrozenBase):
                        r"""TODO docstring for class 'Camera'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        location_range: LocationRange


                class Clutter(StrictFrozenBase):
                        r"""TODO docstring for class 'Clutter'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        initial_location_range: LocationRange


                class Protagonist(StrictFrozenBase):
                        r"""TODO docstring for class 'Protagonist'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        initial_location: Location


                # ------------------------------------------------------
                # ATTRIBUTES
                # ------------------------------------------------------


                camera: Camera
                clutter: Clutter
                protagonist: Protagonist


        class Scene(StrictFrozenBase):
                r"""TODO docstring for class 'Scene'"""


                # ------------------------------------------------------
                # INFRASTRUCTURE
                # ------------------------------------------------------


                class Lighting(StrictFrozenBase):
                        r"""TODO docstring for class 'Lighting'"""


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        ceiling_light: AreaLight
                        window_light: AreaLight


                class Physics(StrictFrozenBase):
                        r"""TODO docstring for class 'Physics'"""


                        # ----------------------------------------------
                        # INFRASTRUCTURE
                        # ----------------------------------------------


                        @pydantic.model_validator(mode='after')
                        def todo_name(self) -> typing.Self:  # TODO name
                                r"""TODO docstring for method 'todo_name'"""

                                if self.frame_end <= self.frame_start:
                                        err = f"TODO err msg"
                                        raise ValueError(err)

                                return self


                        # ----------------------------------------------
                        # ATTRIBUTES
                        # ----------------------------------------------

                        frame_start: PositiveInt
                        frame_end: PositiveInt


                lighting: Lighting
                physics: Physics


        # --------------------------------------------------------------
        # ATTRIBUTES
        # --------------------------------------------------------------

        render: Render
        scene: Scene


def set_up(
        *,
        job_input: JobInput,
        scene_config: SceneConfig,
        fctx: FileContext
) -> None:
        r"""TODO docstring for function 'set_up'"""


        # --------------------------------------------------------------
        # PROTAGONIST
        # --------------------------------------------------------------

        fctx.protagonist.location = mathutils.Vector(
                [
                        scene_config.render.protagonist.initial_location.x,
                        scene_config.render.protagonist.initial_location.y,
                        scene_config.render.protagonist.initial_location.z
                ]
        )
        fctx.protagonist.rotation_euler = (
                math.radians(random.uniform(0, 360)),
                math.radians(random.uniform(0, 360)),
                math.radians(random.uniform(0, 360))
        )


        # --------------------------------------------------------------
        # CLUTTER
        # --------------------------------------------------------------

        for obj in fctx.clutter_collection.objects:
                location = scene_config.render.clutter.initial_location_range.sample()  # TODO line length

                obj.location = mathutils.Vector(
                        [location.x, location.y, location.z]
                )
                obj.rotation_euler = (
                        math.radians(random.uniform(0, 360)),
                        math.radians(random.uniform(0, 360)),
                        math.radians(random.uniform(0, 360))
                )


        # --------------------------------------------------------------
        # SIMULATION
        # --------------------------------------------------------------

        bake_simulation(
                fctx.scene,
                scene_config.scene.physics.frame_start,
                scene_config.scene.physics.frame_end,
                delete_previous=True
        )


def randomise(
        *,
        job_input: JobInput,
        scene_config: SceneConfig,
        image_nr: int,
        fctx: FileContext
) -> None:
        r"""TODO docstring for function 'randomise'"""


        # --------------------------------------------------------------
        # RESET
        # --------------------------------------------------------------

        if (
                image_nr % job_input.scene.additional_keys['reset'] == 0
                and image_nr != 0
        ):
                set_up(
                        job_input=job_input,
                        scene_config=scene_config,
                        fctx=fctx
                )


        # --------------------------------------------------------------
        # CAMERA
        # --------------------------------------------------------------

        location = scene_config.render.camera.location_range.sample()
        lens_sample = job_input.lens.sample()

        fctx.camera.location = mathutils.Vector(
                [location.x, location.y, location.z]
        )
        fctx.camera.data.dof.aperture_fstop = lens_sample.f_stop
        fctx.camera.data.lens = lens_sample.focal_length * 1000


        # --------------------------------------------------------------
        # LIGHTS
        # --------------------------------------------------------------

        # TODO fix

        # ceiling_light = bpy.data.objects['ceiling_light']
        # ceiling_light.location = mathutils.Vector([
        #         random.uniform(*sceneconfig.scene.lighting.ceiling_light.location_range.x),
        #         random.uniform(*sceneconfig.scene.lighting.ceiling_light.location_range.y),
        #         random.uniform(*sceneconfig.scene.lighting.ceiling_light.location_range.z)
        # ])
        # ceiling_light.data.energy = random.uniform(  # TODO fix?
        #         *sceneconfig.scene.lighting.ceiling_light.power_range
        # )
        # ceiling_light.data.temperature = random.uniform(  # TODO fix?
        #         *sceneconfig.scene.lighting.ceiling_light.temperature_range
        # )


        # # ---- Window light ----

        # window_light = bpy.data.objects['window_light']
        # window_light.location = mathutils.Vector([
        #         random.uniform(*sceneconfig.scene.lighting.window_light.location_range.x),
        #         random.uniform(*sceneconfig.scene.lighting.window_light.location_range.y),
        #         random.uniform(*sceneconfig.scene.lighting.window_light.location_range.z)
        # ])
        # window_light.data.energy = random.uniform(  # TODO fix?
        #         *sceneconfig.scene.lighting.window_light.power_range
        # )
        # window_light.data.temperature = random.uniform(  # TODO fix?
        #         *sceneconfig.scene.lighting.window_light.temperature_range
        # )


# ======================================================================
# PUBLIC API
# ======================================================================

__all__ = [
        'SceneConfig',
        'set_up',
        'randomise'
]


#<file:end>
