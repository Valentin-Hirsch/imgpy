# src/imgpy/blender/_common.py
r"""Common Blender functions.

This module provides the following functions:

- :func:`render`
- :func:`set_up`

TODO

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import typing

import bpy

from ._filecontext import FileContext
from ._utils import (
        import_material,
        import_node_tree,
        import_object,
        import_stl,
        set_origin,
        set_shading
)
from .._config import config
from ..models import JobInput
from ..protocols import CyclesPreferences


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def _set_up_misc(job_input: JobInput, fctx: FileContext) -> None:
        r"""Set-up miscellaneous aspects.

        Args:
                job_input (`JobInput`):
                        Job input.
                file_dir (`pathlib.path`):
                        Parent directory of the input file.

        """

        fctx.scene.render.resolution_x = job_input.render.resolution.x
        fctx.scene.render.resolution_y = job_input.render.resolution.y


def _set_up_compositing(
        job_input: JobInput,
        fctx: FileContext
) -> None:
        r"""Set-up the compositing node group.

        Args:
                job_input (`JobInput`):
                        Job input.
                file_dir (`pathlib.path`):
                        Parent directory of the input file.

        Raises:
                ValueError:
                        Invalid render output file format specified in
                        job input.

        """

        file = config.data_dir / 'blender' / 'common' / 'compositing.blend'

        node_tree = import_node_tree(file, use_fake_user=True)

        fctx.scene.compositing_node_group = node_tree

        fctx.register_compositing_node_group()

        fctx.render_layers_node.scene = fctx.scene
        fctx.render_layers_node.layer = fctx.view_layer.name

        fctx.file_output_node.directory = '//render'  # TODO check if correct

        if job_input.render.file_format == 'jpeg':
                fctx.file_output_node.format.file_format = 'JPEG'  # TODO fix? -> create FileOutputNode object protocol
                fctx.file_output_node.format.quality = job_input.render.additional_keys['jpeg_quality']  # TODO fix & line length
        elif job_input.render.file_format == 'png':
                fctx.file_output_node.format.file_format = 'PNG'  # TODO fix?
                fctx.file_output_node.format.quality = job_input.render.additional_keys['png_compression']  # TODO fix & line length
        else:
                err = f"invalid file format {job_input.render.file_format}''"
                raise ValueError(err)


def _set_up_cycles(job_input: JobInput, fctx: FileContext) -> None:
        r"""TODO docstring for function '_set_up_cycles'

        TODO

        Arguments:
                runconfig (RunConfig):
                        Job input.
                fctx (FileContext):
                        Blend file context.

        Raises:
                ValueError:
                        Invalid render device type specified in job
                        input.

        """

        # TODO we assume this as given (i.e. the scene is set up correctly -> implement validation before after loading to check most critical things)
        # if fctx.scene.render.engine != 'CYCLES':
        #         err = f"TODO err msg: render engine is not Cycles {fctx.scene.render.engine}"
        #         raise Exception(err)  # TODO exc type
        # fctx.view_layer.use_pass_object_index = True

        # TODO ultraultr temp fix
        cprefs = fctx.cycles_preferences

        # cprefs = typing.cast(
        #         CyclesPreferences,
        #         fctx._addons['cycles'].preferences
        # )


        cprefs.refresh_devices()

        if job_input.render.device_type == 'cpu':
                fctx._cycles_settings.device = 'CPU'
                cprefs.compute_device_type = 'NONE'

                if job_input.render.additional_keys['threads'] == 0:
                        fctx.scene.render.threads_mode = 'AUTO'
                else:
                        fctx.scene.render.threads_mode = 'FIXED'
                        fctx.scene.render.threads = job_input.render.additional_keys['threads']  # TODO line length
        elif job_input.render.device_type == 'cuda':
                fctx._cycles_settings.device = 'GPU'
                cprefs.compute_device_type = 'CUDA'
        elif job_input.render.device_type == 'optix':
                fctx._cycles_settings.device = 'GPU'
                cprefs.compute_device_type = 'OPTIX'
        elif job_input.render.device_type == 'hip':
                fctx._cycles_settings.device = 'GPU'
                cprefs.compute_device_type = 'HIP'
        else:
                err = (
                        f"invalid render device type "
                        f"'{job_input.render.device_type}'"
                )
                raise ValueError(err)


def _set_up_clutter(job_input: JobInput, fctx: FileContext) -> None:
        r"""TODO docstring fro function '_set_up_clutter'"""

        for oof in job_input.scene.clutter:  # TODO rename oof...


                # ---- Import ----

                file = config.data_dir / 'geometry' / 'clutter' / f'{oof.object}.stl'

                obj = import_stl(
                        file,
                        apply_scale=True,
                        collection=fctx.clutter_collection,
                        scale_factor=oof.scale_factor,
                        use_fake_user=True
                )


                # ---- Material ----

                material = oof.material

                if material not in bpy.data.materials:
                        material_file = (
                                config.data_dir
                                / 'blender'
                                / 'materials'
                                / f'{material}.blend'
                        )
                        mat = import_material(
                                material_file,
                                use_fake_user=True
                        )
                else:
                        mat = bpy.data.materials[material]

                obj.active_material = mat

                # ---- TODO misc ----

                set_origin(obj)

                mod_decimate = typing.cast(
                        bpy.types.DecimateModifier,
                        obj.modifiers.new('mod_decimate', 'DECIMATE')
                )
                mod_decimate.ratio = oof.decimate_ratio

                obj.pass_index = (
                        0 if oof.class_id is None else oof.class_id + 1
                )

                # TODO temp
                set_shading(obj, mode=oof.shade_mode)


                # ---- Rigid body

                # TODO ultra temp!!!!!
                fctx.rbw_collection.objects.link(obj)
                # bpy.data.collections['rigid_body_world'].objects.link(obj)

                rb = typing.cast(
                        bpy.types.RigidBodyObject,
                        obj.rigid_body
                )
                rb.type = 'ACTIVE'
                rb.mass = oof.rigid_body.mass

                if oof.rigid_body.collision_shape == 'convex_hull':
                        rb.collision_shape = 'CONVEX_HULL'
                elif oof.rigid_body.collision_shape == 'mesh':
                        rb.collision_shape = 'MESH'
                else:
                        err = (
                                f"invalid collision shape: "
                                f"'{oof.rigid_body.collision_shape}'"
                        )
                        raise ValueError(err)

                rb.friction = oof.rigid_body.friction
                rb.restitution = oof.rigid_body.restitution


                # ---- Instantiate ----

                for _ in range(oof.count-1):
                        o = obj.copy()
                        fctx.clutter_collection.objects.link(o)


def _load_blend_protagonist(
        file: pathlib.Path,
        job_input: JobInput,
        fctx: FileContext
) -> bpy.types.Object:
        r"""TODO docstring for function '_load_blend_protagonist'

        TODO

        Arguments:
                file (pathlib.Path):
                        Path to the Blend file.
                runconfig (RunConfig):
                        Job input.
                fctx (FileContext):
                        Blend file context.

        Returns:
                obj (bpy.types.Object):
                        Protagonist mesh object.

        Raises:
                TypeError:
                        The data of the imported object is not a mesh.

        """

        obj = import_object(
                file,
                collection=fctx.render_collection,
                name=job_input.protagonist.name,
                use_fake_user=True
        )

        if not isinstance(obj.data, bpy.types.Mesh):
                err = f"not a mesh object: '{type(obj.data)}'"
                raise TypeError(err)

        # TODO we need to do anything else here?

        return obj


def _load_stl_protagnoist(
        file: pathlib.Path,
        job_input: JobInput,
        fctx: FileContext
) -> bpy.types.Object:
        r"""TODO docstring for function '_load_mesh_protagnoist'

        TODO

        Arguments:
                file (pathlib.Path):
                        Path of the STL file.
                data_dir (pathlib.Path):
                        ImgPy data directory.
                runconfig (RunConfig):
                        Job input.
                fctx (FileContext):
                        Blend file context.

        Returns:
                obj (bpy.types.Object):
                        Protagonist mesh object.

        """

        scale_factor = job_input.protagonist.additional_keys['scale_factor']

        obj = import_stl(
                file,
                apply_scale=True,
                collection=fctx.render_collection,
                mesh_name=job_input.protagonist.name,
                object_name=job_input.protagonist.name,
                scale_factor=scale_factor,
                use_fake_user=True
        )


        # ---- Material ----

        material = job_input.protagonist.additional_keys['material']

        if material not in bpy.data.materials:
                material_file = (
                        config.data_dir
                        / 'blender'
                        / 'materials'
                        / f'{material}.blend'
                )
                mat = import_material(
                        material_file,
                        use_fake_user=True
                )
        else:
                mat = bpy.data.materials[material]

        obj.active_material = mat


        # ---- TODO misc ----



        # TODO temp
        set_shading(obj, mode=job_input.protagonist.additional_keys['shade_mode'])

        
        set_origin(obj)

        # if 'decimate_ratio' in runconfig.protagonist.additional_keys:  # TODO optional or required -> possibly remove or reinstate
        mod_decimate = typing.cast(
                bpy.types.DecimateModifier,
                obj.modifiers.new('mod_decimate', 'DECIMATE')
        )
        mod_decimate.ratio = job_input.protagonist.additional_keys[
                'decimate_ratio'
        ]

        return obj


def _set_up_protagonist(
        file: pathlib.Path,
        job_input: JobInput,
        fctx: FileContext
) -> None:
        r"""TODO docstring for function '_set_up_protagonist'

        TODO all docstr

        Arguments:
                file (pathlib.Path):
                        Path of the protagonist file.
                job_input (JobInput):
                        Job input.
                fctx (FileContext):
                        Blend file context.

        Raises:
                ValueError:
                        TODO
                ValueError:
                        TODO

        """


        # --------------------------------------------------------------
        # IMPORT
        # --------------------------------------------------------------

        match file.suffix.lower():
                case '.blend':
                        obj = _load_blend_protagonist(file, job_input, fctx)
                case '.stl':
                        obj = _load_stl_protagnoist(file, job_input, fctx)
                case _:
                        err = f"unsupported file type '{file.as_posix()}'"
                        raise ValueError(err)


        # ---- TODO misc ----

        fctx.register_protagonist(obj)
        fctx.protagonist.pass_index = job_input.protagonist.class_id + 1

        # TODO fix
        # mesh = typing.cast(bpy.types.Mesh, obj.data)
        # mesh.shade_smooth()  # TODO temp -> fix with auto smooth
        # mesh.shade_flat()  # TODO temp -> fix with auto smooth

        


        # ---- Rigid body ----

        #fctx.rigid_body_world_collection.objects.link(obj)  # TODO now included in register_protagonist

        fctx.rbw_collection.objects.link(obj)

        rb = typing.cast(
                bpy.types.RigidBodyObject,
                fctx.protagonist.rigid_body
        )
        rb.type = 'ACTIVE'
        rb.mass = job_input.protagonist.rigid_body.mass

        match job_input.protagonist.rigid_body.collision_shape:
                case 'convex_hull':
                        rb.collision_shape = 'CONVEX_HULL'
                case 'mesh':
                        rb.collision_shape = 'MESH'
                case _:
                        err = (
                                f"invalid collision shape "
                                f"'{job_input.protagonist.rigid_body.collision_shape}'"  # TODO line length
                        )
                        raise ValueError(err)

        rb.friction = job_input.protagonist.rigid_body.friction
        rb.restitution = job_input.protagonist.rigid_body.restitution


        # ---- Camera tracking ----

        cst_track_to = typing.cast(
                bpy.types.TrackToConstraint,
                fctx.camera.constraints.new('TRACK_TO')
        )
        cst_track_to.target = fctx.protagonist

        fctx.camera.data.dof.focus_object = fctx.protagonist  # TODO fix?


# ======================================================================
# SETUP
# ======================================================================


def set_up(job_input: JobInput, file_dir: pathlib.Path) -> FileContext:
        r"""Set up a Blender file.

        Args:
                job_input (`JobInput`):
                        Job input.
                file_dir (`pathlib.path`):
                        Parent directory of the input file.

        Returns:
                `FileContext`:
                        Blender file context.

        """

        fctx = FileContext(job_input)

        protagonist_file = file_dir / job_input.protagonist.file

        _set_up_protagonist(protagonist_file, job_input, fctx)
        _set_up_clutter(job_input, fctx)
        _set_up_compositing(job_input, fctx)
        _set_up_cycles(job_input, fctx)
        _set_up_misc(job_input, fctx)

        if not fctx.check_ready():
                err = f"TODO err msg"
                raise RuntimeError(err)

        return fctx


# ======================================================================
# RENDERING
# ======================================================================


def render(prefix: str, fctx: FileContext) -> None:
        r"""Render an image and mask.

        Args:
                prefix (`str`):
                        Image and mask prefix.
                fctx (`FileContext`):
                        Blender file context.

        """

        fctx.file_output_node.file_name = prefix

        bpy.ops.render.render()


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'set_up',
        'render'
]


#<file:end>
