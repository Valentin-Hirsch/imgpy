# src/imgpy/blender/_operators.py
r"""TODO High-level utilities and wrappers for Blender operators.

TODO

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import typing

import bpy
import mathutils  # pyright: ignore[reportMissingModuleSource]


# ======================================================================
# IMPORT OPERATORS
# ======================================================================


def import_material(
        file: pathlib.Path,
        *,
        name: str | None = None,
        use_fake_user: bool = False
) -> bpy.types.Material:
        r"""Import a material from a Blend file.

        **Important:**

        - Only the material name is validated. Any dependencies imported
          with it are managed by Blender's built-in library-loading
          functionality and will be renamed if name collisions occur.
        - If `use_fake_user` is `False` the imported material has zero
          users which will cause it to be removed on the next save.

        Arguments:
                file (pathlib.Path):
                        Path of the Blend file containing the material.
                name (str | None):
                        Name of the material to import. If `None`,
                        `file.stem` is used (default: `None`).
                use_fake_user (bool):
                        Add a fake user to the imported material
                        (default: `False`).

        Returns:
                mat (bpy.types.Material):
                        Imported material.

        Raises:
                LookupError:
                        No material with the requested name exists in
                        the Blend file.
                ValueError:
                        A material with the requested name already
                        exists in the current Blend file.

        """

        if name is None:
                name = file.stem

        if name in bpy.data.materials:
                err = f"material with name already exists: '{name}'"
                raise ValueError(err)

        with bpy.data.libraries.load(  # pyright: ignore[reportGeneralTypeIssues]
                file.resolve().as_posix(),
                link=False
        ) as (src, dst):
                if name not in src.materials:
                        err = f"no material with name: '{name}'"
                        raise LookupError(err)

                dst.materials = [name]

        mat = typing.cast(bpy.types.Material, dst.materials[0])
        mat.use_fake_user = use_fake_user

        return mat


def import_node_tree(
        file: pathlib.Path,
        *,
        name: str | None = None,
        use_fake_user: bool = False
) -> bpy.types.NodeTree:
        r"""Import a node tree from a Blend file.

        **Important:**

        - Only the node tree name is validated. Any dependencies
          imported with it are managed by Blender's built-in library-
          loading functionality and will be renamed if name collisions
          occur.
        - If `use_fake_user` is `False` the imported node tree has zero
          users which will cause it to be removed on the next save.

        Arguments:
                file (pathlib.Path):
                        Path of the Blend file containing the node tree.
                name (str | None):
                        Name of the node tree to import. If `None`,
                        `file.stem` is used (default: `None`).
                use_fake_user (bool):
                        Add a fake user to the imported node tree
                        (default: `False`).

        Returns:
                ntr (bpy.types.NodeTree):
                        Imported node tree.

        Raises:
                LookupError:
                        No node tree with the requested name exists in
                        the Blend file.
                ValueError:
                        A node tree with the requested name already
                        exists in the current Blend file.

        """

        if name is None:
                name = file.stem

        if name in bpy.data.node_groups:
                err = f"node tree with name already exists: '{name}'"
                raise ValueError(err)

        with bpy.data.libraries.load(  # pyright: ignore[reportGeneralTypeIssues]
                file.resolve().as_posix(),
                link=False
        ) as (src, dst):
                if name not in src.node_groups:
                        err = f"no node tree with name: '{name}'"
                        raise LookupError(err)

                dst.node_groups = [name]

        ntr = typing.cast(bpy.types.NodeTree, dst.node_groups[0])
        ntr.use_fake_user = use_fake_user

        return ntr


def import_object(
        file: pathlib.Path,
        *,
        collection: bpy.types.Collection | None = None,
        name: str | None = None,
        use_fake_user: bool = False
) -> bpy.types.Object:
        r"""Import an object from a Blend file.

        **Important:**

        - Only the object name is validated. Any dependencies imported
          with it are managed by Blender's built-in library-loading
          functionality and will be renamed if name collisions occur.
        - If `collection` is `None`, the imported object is not added to
          any collection. If `use_fake_user` is `False`, this results in
          an object with zero users which will cause it to be removed on
          the next save.

        Arguments:
                file (pathlib.Path):
                        Path of the Blend file containing the object.
                collection (bpy.types.Collection | None):
                        Collection to link the imported object to. If
                        `None`, the object is not linked to any
                        collection (default: `None`).
                name (str | None): 
                        Name of the object to import. If `None`,
                        `file.stem` is used (default: `None`).
                use_fake_user (bool):
                        Add a fake user to the imported object (default:
                        `False`).

        Returns:
                obj (bpy.types.Object):
                        Imported object.

        Raises:
                LookupError:
                        No object with the requested name exists in the
                        Blend file.
                ValueError:
                        An object with the requested name already exists
                        in the current Blend file.

        """

        if name is None:
                name = file.stem

        if name in bpy.data.objects:
                err = f"object with name already exists: '{name}'"
                raise ValueError(err)

        with bpy.data.libraries.load(  # pyright: ignore[reportGeneralTypeIssues]
                file.resolve().as_posix(),
                link=False
        ) as (src, dst):
                if name not in src.objects:
                        err = f"no object with name: '{name}'"
                        raise LookupError(err)

                dst.objects = [name]

        obj = typing.cast(bpy.types.Object, dst.objects[0])
        obj.use_fake_user = use_fake_user

        if collection is not None:
                collection.objects.link(obj)

        return obj


def import_stl(
        file: pathlib.Path,
        *,
        apply_scale: bool = True,
        collection: bpy.types.Collection | None = None,
        mesh_name: str | None = None,
        object_name: str | None = None,
        scale_factor: float = 1,
        use_fake_user: bool = False
) -> bpy.types.Object:
        r"""Import a mesh from an STL file.

        This function imports the mesh from an STL file and creates an
        object using the imported mesh as the data.

        **Important:**

        - Both the object and mesh name are validated.
        - If `collection` is `None`, the created object is not added to
          any collection. If `use_fake_user` is `False`, this results in
          an object with zero users which will cause it to be removed on
          the next save.

        Arguments:
                file (pathlib.Path):
                        Path of the STL file.
                apply_scale (bool):
                        Apply the created object's scale transform to
                        the imported mesh (default: `True`).
                collection (bpy.types.Collection | None):
                        Collection to link the created object to. If
                        `None`, the object is not linked to any
                        collection (default: `None`).
                mesh_name (str | None):
                        Name of the imported mesh. If `None`, Blender
                        derives a name from the file name (default:
                        `None`).
                object_name (str | None):
                        Name of the created object. If `None`, Blender
                        derives a name from the file name (default:
                        `None`).
                scale_factor (float):
                        STL import scale factor (default: `1`).
                use_fake_user (bool):
                        Add a fake user to the created object (default:
                        `False`).

        Returns:
                obj (bpy.types.Object):
                        Imported mesh object.

        Raises:
                ValueError:
                        An object or mesh with the requested name
                        already exists in the current Blend file.
                RuntimeError:
                        STL import created multiple objects.


        """

        if mesh_name is not None and mesh_name in bpy.data.meshes:
                err = f"mesh with name already exists: '{mesh_name}'"
                raise ValueError(err)

        if object_name is not None and object_name in bpy.data.objects:
                err = f"object with name already exists: '{object_name}'"
                raise ValueError(err)

        objs_before = set(bpy.data.objects)

        bpy.ops.wm.stl_import(
                filepath=file.resolve().as_posix(),
                global_scale=scale_factor
        )

        objs_after = set(bpy.data.objects) - objs_before
        if len(objs_after) != 1:
                err = f"STL import created multiple objects: {len(objs_after)}"
                raise RuntimeError(err)

        obj, = objs_after
        obj.use_fake_user = use_fake_user
        mesh = typing.cast(bpy.types.Mesh, obj.data)

        if apply_scale:
                apply_scale_transform(obj)

        for col in list(obj.users_collection):
                col.objects.unlink(obj)

        if collection is not None:
                collection.objects.link(obj)

        if mesh_name is not None:
                mesh.name = mesh_name

        if object_name is not None:
                obj.name = object_name

        return obj


# ======================================================================
# UTILITY OPERATORS
# ======================================================================



# from src.blender._config import config
# from src.blender._exceptions import BlenderOperatorError


from .._config import config





def apply_transforms(
        obj: bpy.types.Object,
        *,
        location: bool = True,
        rotation: bool = True,
        scale: bool = True,
) -> None:
        r"""TODO docstring"""

        ctx = bpy.context.copy()

        ctx['selected_editable_objects'] = [obj]

        with bpy.context.temp_override(**ctx) as override:
                if config.override_logging:
                        override.logging_set(True, hide_missing=False)

                result = bpy.ops.object.transform_apply(
                        location=location,
                        rotation=rotation,
                        scale=scale
                )

        if 'FINISHED' not in result:
                err = (
                        f"failed to apply transforms to object 'obj': "
                        f"name='{obj.name}', type='{obj.type}', result={result}"
                )
                raise BlenderOperatorError(err)




def apply_scale_transform(obj: bpy.types.Object) -> None:
        r"""Apply an object's scale transformation.

        TODO

        **Important:**

        - Supported object types:
          - Mesh
        - ~~This function only applys the scale encoded by TODO....~~
        - TODO this function uses context overrides, no clue if that works correctly...

        Arguments:
                obj (bpy.types.Object):
                        TODO

        Raises:
                TypeError: TODO

        """

        if not isinstance(obj.data, bpy.types.Mesh):
                err = f"not a mesh object: '{type(obj.data)}'"
                raise TypeError(err)

        # TODO what overrides do we actually need?
        ctx = bpy.context.copy()
        ctx['active_ovject'] = obj
        ctx['object'] = obj
        ctx['selected_editable_objects']
        ctx['selected_objects'] = [obj]

        with bpy.context.temp_override(**ctx) as override:
                #override.logging_set(True, hide_missing=False)  # TODO logging

                bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)


def bake_simulation(
        scene: bpy.types.Scene,
        frame_start: int | None = None,
        frame_end: int | None = None,
        *,
        delete_previous: bool = False
) -> None:
        r"""TODO docstring

        TODO

        **Important:**

        - TODO this function uses context overrides, no clue if that works correctly...

        TODO REDO WHOLE DOCSTR

        Arguments:
                scene (bpy.types.Scene):
                        TODO
                frame_end (int | None):
                        TODO (default: `None`).
                frame_end (int | None):
                        TODO (default: `None`).

        """

        # TODO doesn't seem to set the start/end correctly?!
        if frame_end is not None:
                scene.frame_end = frame_end

        if frame_start is not None:
                scene.frame_start = frame_start

        # TODO what overrides do we actually need?
        ctx = bpy.context.copy()
        ctx['scene'] = scene

        with bpy.context.temp_override(**ctx) as override:
                #override.logging_set(True, hide_missing=False)  # TODO logging

                if delete_previous:
                        bpy.ops.ptcache.free_bake_all()

                bpy.ops.ptcache.bake_all()

        scene.frame_set(scene.frame_end)


def set_origin(
        obj: bpy.types.Object,
        *,
        mode: typing.Literal['origin_to_geometry'] = 'origin_to_geometry'
) -> None:
        r"""TODO docstring
        
        TODO 

        **Important:**

        - Supported object types:
          - Mesh
        
        Arguments:
                obj (bpy.types.Object):
                        TODO
                mode (str):  # str or typing.Literal?
                        TODO

        Raises:
                TypeError:
                        TODO
                ValueError:
                        TODO

        """

        ctx = bpy.context.copy()
        # TODO I don't think these are needed
        # ctx['active_ovject'] = obj
        # ctx['object'] = obj
        ctx['selected_editable_objects'] = [obj]
        ctx['selected_objects'] = [obj]

        with bpy.context.temp_override(**ctx) as override:
                override.logging_set(True, hide_missing=False)  # TODO logging
                bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')




        return  # TODO temp fix

        if not isinstance(obj.data, bpy.types.Mesh):
                err = f"not a mesh object: '{type(obj.data)}'"
                raise TypeError(err)

        mesh = obj.data

        if mode == 'origin_to_geometry':
                centre = sum(
                        (v.co for v in mesh.vertices),
                        start=mathutils.Vector()  # TODO before was mesh.vertices[0].co.copy()
                )
                centre /= len(mesh.vertices)
                mesh.transform(mathutils.Matrix.Translation(-centre))  # TODO fox?
                obj.matrix_world.translation += (
                        obj.matrix_world.to_3x3()
                        @ centre
                )
        else:
                err = f"invalid mode: '{mode}'"
                raise ValueError(err)


def set_shading(
        obj: bpy.types.Object,
        *,
        mode: typing.Literal['smooth', 'auto_smooth', 'flat'] = 'smooth'
) -> None:
        r"""TODO docstring
        
        TODO mode `auto_smooth` uses operator and context overloading!

        """

        if not isinstance(obj.data, bpy.types.Mesh):
                err = f"not a mesh object: '{type(obj.data)}'"
                raise TypeError(err)

        mesh = obj.data

        if mode == 'smooth':
                mesh.shade_smooth()
        elif mode == 'auto_smooth':
                # TODO what overrides do we actually need?
                ctx = bpy.context.copy()
                ctx['selected_objects'] = [obj]

                with bpy.context.temp_override(**ctx) as override:
                        override.logging_set(True, hide_missing=False)  # TODO logging
                        bpy.ops.object.shade_auto_smooth()
        elif mode == 'flat':
                mesh.shade_flat()
        else:
                err = f"invalid mode: '{mode}'"
                raise ValueError(err)









# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = [
        'import_material',
        'import_node_tree',
        'import_object',
        'import_stl',
        'bake_simulation',





        'apply_transforms',



        'apply_scale_transform',
        'set_origin',
        'set_shading'
]


#<file:end>
