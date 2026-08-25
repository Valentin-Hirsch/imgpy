# src/imgpy/blender/_filecontext.py
r"""Blender file context.

This module provides the :class:`FileContext` class.

This class provides safe access to a Blender file.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import typing

import bpy

from ..models import JobInput
from ..protocols import CyclesPreferences, CyclesSettings


# ======================================================================
# FILECONTEXT
# ======================================================================


class FileContext:
        r"""Blender file context."""


        # --------------------------------------------------------------
        # INFRASTRUCTURE
        # --------------------------------------------------------------

        __slots__ = (
                '_camera',
                '_clutter_collection',
                '_compositing_node_group',
                '_cycles_preferences',
                '_cycles_settings',
                '_file_output_node',
                '_instance_classes',
                '_job_input',
                '_next_pass_index',
                '_protagonist',
                '_rbw_collection',
                '_render_collection',
                '_render_layers_node',
                '_scene',
                '_view_layer'
        )


        def __init__(self, job_input: JobInput) -> None:
                r"""Initialise instance of `FileContext`.

                Args:
                        job_input (`JobInput`):
                                Job input.

                """

                self._job_input = job_input

                self._register_scene_file()

                self._compositing_node_group = None
                self._file_output_node = None
                self._render_layers_node = None

                self._protagonist = None

                # Pass index '0' is reserved for background/unlabelled
                # objects (see 'register_instance').
                self._next_pass_index = 1
                self._instance_classes = {}


        # --------------------------------------------------------------
        # PROPERRTIES
        # --------------------------------------------------------------


        @property
        def camera(self) -> bpy.types.Object:
                r"""Camera.

                Returns:
                        `bpy.types.Object`:
                                Camera (`type(camera.data) ==
                                bpy.types.Camera`).

                """

                return self._camera


        @property
        def clutter_collection(self) -> bpy.types.Collection:
                r"""Clutter collection.

                Returns:
                        `bpy.types.Collection`:
                                Clutter collection.

                """

                return self._clutter_collection


        @property
        def compositing_node_group(self) -> bpy.types.NodeTree:
                r"""Compositing node group.

                Returns:
                        `bpy.types.NodeTree`:
                                Compositing node group.

                Raises:
                        `RuntimeError`:
                                No compositing node group registered.

                """

                if self._compositing_node_group is None:
                        err = f"no compositing node group registered"
                        raise RuntimeError(err)

                return self._compositing_node_group


        @property
        def cycles_preferences(self) -> CyclesPreferences:
                r"""Cycles preferences.

                Returns:
                        `CyclesPreferences`:
                                Cycles preferences.

                """

                return self._cycles_preferences


        @property
        def cycles_settings(self) -> CyclesSettings:
                r"""Cycles settings.

                Returns:
                        `CyclesSettings`:
                                Cycles settings.

                """

                return self._cycles_settings


        @property
        def file_output_node(self) -> bpy.types.CompositorNodeOutputFile:
                r"""File output node.

                Returns:
                        `bpy.types.CompositorNodeOutputFile`:
                                File output node.

                Raises:
                        `RuntimeError`:
                                No file output node registered.

                """

                if self._file_output_node is None:
                        err = f"no file output node registered"
                        raise RuntimeError(err)

                return self._file_output_node


        @property
        def instance_classes(self) -> dict[int, int]:
                r"""Object-instance-to-class mapping.

                Maps each unique object-index (`pass_index`) value
                assigned via `register_instance` to the YOLO class id
                of the object instance it identifies. Background/
                unlabelled objects (`pass_index` `0`) are not included.

                Returns:
                        `dict[int, int]`:
                                Mapping of `pass_index` to `class_id`.

                """

                return self._instance_classes


        @property
        def protagonist(self) -> bpy.types.Object:
                r"""Protagonist.

                Returns:
                        `bpy.types.Object`:
                                Protagonist (`type(protagonist.data) ==
                                bpy.types.Mesh`).

                """

                if self._protagonist is None:
                        err = f"no protagonist registered"
                        raise RuntimeError(err)

                return self._protagonist


        @property
        def rbw_collection(self) -> bpy.types.Collection:
                r"""Rigid body world collection.

                Returns:
                        `bpy.types.Collection`:
                                Rigid body world collection.

                """

                return self._rbw_collection


        @property
        def render_collection(self) -> bpy.types.Collection:
                r"""Render collection.

                Returns:
                        `bpy.types.Collection`:
                                Render collection.

                """

                return self._render_collection


        @property
        def render_layers_node(self) -> bpy.types.CompositorNodeRLayers:
                r"""Render layers node.

                Returns:
                        `bpy.types.CompositorNodeRLayers`:
                                Render layers.

                Raises:
                        `RuntimeError`:
                                No render layers node registered.

                """

                if self._render_layers_node is None:
                        err = f"no render layers node registered"
                        raise RuntimeError(err)

                return self._render_layers_node


        @property
        def scene(self) -> bpy.types.Scene:
                r"""Scene.

                Returns:
                        `bpy.types.Scene`:
                                Scene.

                """

                return self._scene


        @property
        def view_layer(self) -> bpy.types.ViewLayer:
                r"""View layer.

                Returns:
                        `bpy.types.ViewLayer`:
                                View layer.

                """

                return self._view_layer


        # --------------------------------------------------------------
        # PUBLIC METHODS
        # --------------------------------------------------------------


        def check_ready(self) -> bool:
                r"""Check if the Blender file context is ready.

                Returns:
                        `bool`:
                                TODO

                """

                if self._compositing_node_group is None:
                        return False

                if self._file_output_node is None:
                        return False

                if self._render_layers_node is None:
                        return False

                if self._protagonist is None:
                        return False

                return True


        def register_compositing_node_group(self) -> None:
                r"""Register the compositing node group."""

                if self._compositing_node_group is not None:
                        err = (
                                "compositing node group has already been "
                                "registered"
                        )
                        raise RuntimeError(err)

                if (node_group := self.scene.compositing_node_group) is None:
                        err = "scene has no compositing node group"
                        raise RuntimeError(err)
                else:
                        self._compositing_node_group = node_group

                self._file_output_node = typing.cast(
                        bpy.types.CompositorNodeOutputFile,
                        self.compositing_node_group.nodes['file_output']
                )

                self._render_layers_node = typing.cast(
                        bpy.types.CompositorNodeRLayers,
                        self.compositing_node_group.nodes['render_layers']
                )


        def register_instance(self, class_id: int) -> int:
                r"""Register a labelled object instance.

                Each call allocates a new, globally unique object-index
                (`pass_index`) value for one physical object instance
                (protagonist or a single clutter object/copy) and
                records its class id. Assigning a unique `pass_index`
                per *instance* (rather than reusing the same value for
                every instance of a class) ensures that the rendered
                object-index mask distinguishes touching or overlapping
                instances of the same class, instead of merging them
                into a single mask region.

                Args:
                        class_id (`int`):
                                YOLO class id of the object instance.

                Returns:
                        `int`:
                                Unique `pass_index` value to assign to
                                the object instance. Pass index `0` is
                                never returned; it is reserved for
                                background/unlabelled objects.

                """

                pass_index = self._next_pass_index
                self._next_pass_index += 1

                self._instance_classes[pass_index] = class_id

                return pass_index


        def register_protagonist(self, obj: bpy.types.Object) -> None:
                r"""Register the protagonist.

                Args:
                        obj (`bpy.types.Object`):
                                Protagonist (`type(obj.data) ==
                                bpy.types.Mesh`).

                """

                if self._protagonist is not None:
                        err = "protagonist has already been registered"
                        raise RuntimeError(err)

                if not isinstance(obj, bpy.types.Object):
                        err = "not a Blender object"
                        raise TypeError(err)

                if not isinstance(obj.data, bpy.types.Mesh):
                        err = "data is not a mesh"
                        raise TypeError(err)

                self._protagonist = obj


        # --------------------------------------------------------------
        # PRIVATE METHODS
        # --------------------------------------------------------------


        def _register_scene_file(self) -> None:
                r"""Register the scene file."""

                if (scene := bpy.context.scene) is None:
                        err = "Blender file has no scene"
                        raise RuntimeError(err)
                else:
                        self._scene = scene

                if (camera := self.scene.camera) is None:
                        err = "scene has no camera"
                        raise RuntimeError(err)
                else:
                        self._camera = camera

                if (view_layer := bpy.context.view_layer) is None:
                        err = f"Blender file has no context"
                        raise RuntimeError(err)
                else:
                        self._view_layer = view_layer

                self._cycles_preferences = bpy.context.preferences.addons[
                        'cycles'
                ].preferences
                self._cycles_settings = self.scene.cycles

                self._clutter_collection = bpy.data.collections['clutter']
                self._render_collection = bpy.data.collections['render']

                self._rbw_collection = bpy.data.collections['rigid_body_world']


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['FileContext']


#<file:end>
