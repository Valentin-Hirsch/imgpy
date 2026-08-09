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

import bpy
import mathutils  # pyright: ignore[reportMissingModuleSource]
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

                        area_1: AreaLight
                        area_2: AreaLight
                        area_3: AreaLight
                        area_4: AreaLight
                        spot: SpotLight


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


                # ------------------------------------------------------
                # ATTRIBUTES
                # ------------------------------------------------------

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

        # TODO add lights to scene and randomise them

        area_1 = bpy.data.objects['area_1']

        area_1.data.energy = random.uniform(*scene_config.scene.lighting.area_1.power_range)
        area_1.data.temperature = random.uniform(*scene_config.scene.lighting.area_1.temperature_range)

        area_2 = bpy.data.objects['area_2']

        area_2.data.energy = random.uniform(*scene_config.scene.lighting.area_2.power_range)
        area_2.data.temperature = random.uniform(*scene_config.scene.lighting.area_2.temperature_range)

        area_3 = bpy.data.objects['area_3']

        area_3.data.energy = random.uniform(*scene_config.scene.lighting.area_3.power_range)
        area_3.data.temperature = random.uniform(*scene_config.scene.lighting.area_3.temperature_range)

        area_4 = bpy.data.objects['area_4']

        area_4.data.energy = random.uniform(*scene_config.scene.lighting.area_4.power_range)
        area_4.data.temperature = random.uniform(*scene_config.scene.lighting.area_4.temperature_range)

        spot = bpy.data.objects['spot']

        location = scene_config.scene.lighting.spot.location_range.sample()

        spot.location = mathutils.Vector([location.x, location.y, location.z])
        spot.data.energy = random.uniform(*scene_config.scene.lighting.spot.power_range)
        spot.data.temperature = random.uniform(*scene_config.scene.lighting.spot.temperature_range)




# ======================================================================
# PUBLIC API
# ======================================================================

__all__ = [
        'SceneConfig',
        'set_up',
        'randomise'
]


#<file:end>
