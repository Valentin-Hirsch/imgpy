# src/post/_yolo.py
"""Post-processing of rendered images for YOLO datasets.

This module provides the :func:`yolo` function.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import os

# Must be set before 'cv2' is imported: OpenCV's EXR codec is disabled
# by default for security reasons and can only be toggled at import
# time. Masks are stored as EXR (see 'data/blender/common/compositing.
# blend') since 8-bit PNG mask output goes through Blender's display
# color management (gamma/view-transform), which silently corrupts
# the raw object-instance-id pixel encoding for anything but the
# endpoint values 0 and 255.
os.environ.setdefault('OPENCV_IO_ENABLE_OPENEXR', '1')

import pathlib
import random
import shutil
import typing

import cv2
import numpy as np

from .models import JobInput
from src.common import NonNegativeInt, PositiveInt, load_json


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def _load_class_map(in_dir: pathlib.Path) -> dict[int, int]:
        r"""Load the object-instance-to-class mapping for a render job.

        Each rendered mask encodes, per pixel, the unique object-index
        ('pass_index') of the object instance visible there (see
        'src.imgpy.blender.FileContext.register_instance'). This
        mapping recovers the YOLO class id for each such instance id;
        it is written by the rendering job (see 'src.imgpy._core.
        render_images') next to the masks it describes.

        Args:
                in_dir (`pathlib.Path`):
                        Directory containing image and mask files.

        Returns:
                `dict[int, int]`:
                        Mapping of instance id ('pass_index') to
                        `class_id`.

        Raises:
                `FileNotFoundError`:
                        No class map file exists in `in_dir`.

        """

        class_map_file = in_dir / 'classes.json'

        if not class_map_file.is_file():
                err = f"no class map: '{class_map_file.as_posix()}'"
                raise FileNotFoundError(err)

        return {
                int(instance_id): int(class_id)
                for instance_id, class_id in load_json(class_map_file).items()
        }


def _yolo_box(
        pair: tuple[pathlib.Path, pathlib.Path],
        images_dir: pathlib.Path,
        labels_dir: pathlib.Path,
        visualise_dir: pathlib.Path | None,
        job_input: JobInput,
        class_map: dict[int, int]
) -> None:
        r"""TODO docstring for function '_yolo_box'

        Args:
                pair (`tuple[pathlib.Path, pathlib.Path]`):
                        TODO
                images_dir (`pathlib.Path`):
                        TODO
                labels_dir (`pathlib.Path`):
                        TODO
                visualise_dir (`pathlib.Path | None`):
                        TODO
                job_input (`JobInput`):
                        TODO
                class_map (`dict[int, int]`):
                        Mapping of mask instance id to `class_id` (see
                        `_load_class_map`).

        Raises:
                `FileNotFoundError`:
                        Failed to read mask file.

        """

        # TODO refactor (incl. docstring)


        # ---- Unpack arguments and job input ----

        image_file = pair[0]
        mask_file = pair[1]

        create_empty = typing.cast(
                bool,
                job_input.additional_keys['create_empty']
        )
        min_component_area = typing.cast(
                PositiveInt,
                job_input.additional_keys['min_component_area']
        )


        # ---- Copy image file ----

        shutil.copy2(image_file, images_dir / image_file.name)


        # ---- Create label file ----

        label_file = labels_dir / f'{image_file.stem}.txt'

        mask_raw = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)

        if mask_raw is None:
                err = f"failed to read mask: '{mask_file.as_posix()}'"
                raise FileNotFoundError(err)

        # 'mask' is a 2D NumPy array whose pixel values encode the
        # unique object *instance* visible at that pixel (pixel value =
        # 'pass_index'; '0' is background/unlabelled). Each instance
        # id maps to exactly one 'class_id' via 'class_map', so
        # instances of the same class never share a pixel value -
        # touching or overlapping objects of the same class remain
        # distinct connected components below. The EXR mask stores
        # this as an exact (integer-valued) float, so round rather
        # than truncate.
        #
        # mask = [
        #         [int, ...], -> line of the image
        #         ...
        # ]

        if mask_raw.ndim == 3:
                mask_raw = mask_raw[..., 0]

        mask = np.rint(mask_raw).astype(np.int32)

        shape: tuple[int, int] = mask.shape
        height = shape[0]
        width = shape[1]

        annotations: list[str] = []
        boxes: list[tuple[int, int, int, int]] = []

        for value in np.unique(mask):
                if value == 0:
                        continue

                class_id = class_map[int(value)]
                class_mask = (mask == value).astype(np.uint8)

                n_labels, _, stats, _ = cv2.connectedComponentsWithStats(
                        class_mask,
                        connectivity=8
                )

                for label in range(1, n_labels):
                        area = stats[label, cv2.CC_STAT_AREA]

                        if area < min_component_area:
                                continue

                        x_min = int(stats[label, cv2.CC_STAT_LEFT])
                        y_min = int(stats[label, cv2.CC_STAT_TOP])
                        x_max = x_min + int(stats[label, cv2.CC_STAT_WIDTH]) - 1
                        y_max = y_min + int(stats[label, cv2.CC_STAT_HEIGHT]) - 1

                        annotations.append(
                                f'{class_id} '
                                f'{(x_min + x_max + 1) / (2 * width):.6f} '
                                f'{(y_min + y_max + 1) / (2 * height):.6f} '
                                f'{(x_max - x_min + 1) / width:.6f} '
                                f'{(y_max - y_min + 1) / height:.6f}\n'
                        )
                        boxes.append((x_min, y_min, x_max, y_max))

        if not annotations:
                if create_empty:
                        with label_file.open(mode='x', encoding='utf-8') as fp:
                                fp.write('\n')

                return

        with label_file.open(mode='x', encoding='utf-8') as fp:
                fp.writelines(annotations)


        # ---- Visualisation ----

        if visualise_dir is not None:
                visualise_file = visualise_dir / f'{mask_file.stem}_box.png'

                visualisation = cv2.cvtColor(
                        ((mask > 0) * 255).astype(np.uint8),
                        cv2.COLOR_GRAY2BGR
                )

                for x_min, y_min, x_max, y_max in boxes:
                        cv2.rectangle(
                                        visualisation,
                                        (x_min, y_min),
                                        (x_max, y_max),
                                        (0, 0, 255),  # red
                                        2
                                )

                cv2.imwrite(visualise_file, visualisation)


def _yolo_poly(
        pair: tuple[pathlib.Path, pathlib.Path],
        images_dir: pathlib.Path,
        labels_dir: pathlib.Path,
        visualise_dir: pathlib.Path | None,
        job_input: JobInput,
        class_map: dict[int, int]
) -> None:
        r"""TODO docstring for function '_yolo_poly'

        Args:
                pair (`tuple[pathlib.Path, pathlib.Path]`):
                        TODO
                images_dir (`pathlib.Path`):
                        TODO
                labels_dir (`pathlib.Path`):
                        TODO
                visualise_dir (`pathlib.Path | None`):
                        TODO
                job_input (`JobInput`):
                        TODO
                class_map (`dict[int, int]`):
                        Mapping of mask instance id to `class_id` (see
                        `_load_class_map`).

        Raises:
                `FileNotFoundError`:
                        Failed to read mask file.

        """

        # TODO refactor (incl. docstring)


        # ---- Unpack arguments and job input ----

        image_file = pair[0]
        mask_file = pair[1]

        create_empty = typing.cast(
                bool,
                job_input.additional_keys['create_empty']
        )
        min_component_area = typing.cast(
                PositiveInt,
                job_input.additional_keys['min_component_area']
        )
        simplify = typing.cast(float, job_input.additional_keys['simplify'])  # TODO PositiveFloat?


        # ---- Copy image file ----

        shutil.copy2(image_file, images_dir / image_file.name)


        # ---- Create label file ----

        label_file = labels_dir / f'{image_file.stem}.txt'

        mask_raw = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)

        if mask_raw is None:
                err = f"failed to read mask: '{mask_file.as_posix()}'"
                raise FileNotFoundError(err)

        # 'mask' is a 2D NumPy array whose pixel values encode the
        # unique object *instance* visible at that pixel (pixel value =
        # 'pass_index'; '0' is background/unlabelled). Each instance
        # id maps to exactly one 'class_id' via 'class_map', so
        # instances of the same class never share a pixel value -
        # touching or overlapping objects of the same class remain
        # distinct connected components below. The EXR mask stores
        # this as an exact (integer-valued) float, so round rather
        # than truncate.
        #
        # mask = [
        #         [int, ...], -> line of the image
        #         ...
        # ]

        if mask_raw.ndim == 3:
                mask_raw = mask_raw[..., 0]

        mask = np.rint(mask_raw).astype(np.int32)

        shape: tuple[int, int] = mask.shape
        height = shape[0]
        width = shape[1]

        annotations: list[str] = []
        polygons: list[np.ndarray] = []

        for value in np.unique(mask):
                if value == 0:
                        continue

                class_id = class_map[int(value)]
                class_mask = (mask == value).astype(np.uint8)

                n_labels, labels = cv2.connectedComponents(
                        class_mask,
                        connectivity=8
                )

                for label in range(1, n_labels):
                        component = (labels == label).astype(np.uint8)

                        if int(component.sum()) < min_component_area:
                                continue

                        contours, _ = cv2.findContours(
                                component,
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_NONE,
                        )

                        contour = max(contours, key=cv2.contourArea)

                        epsilon = simplify * cv2.arcLength(contour, True)
                        contour = cv2.approxPolyDP(contour, epsilon, True)

                        coords: list[str] = []

                        for x, y in contour[:, 0]:
                                coords.append(f'{x / width:.6f}')
                                coords.append(f'{y / height:.6f}')

                        annotations.append(f'{class_id} ' + ' '.join(coords) + '\n')
                        polygons.append(contour)

        if not annotations:
                if create_empty:
                        with label_file.open(mode='x', encoding='utf-8') as fp:
                                fp.write('\n')

                return

        with label_file.open(mode='x', encoding='utf-8') as fp:
                fp.writelines(annotations)


        # ---- Visualisation ----

        if visualise_dir is not None:
                polygon_file = visualise_dir / f'{mask_file.stem}_polygon.png'

                vis_polygon = cv2.cvtColor(
                        ((mask > 0) * 255).astype(np.uint8),
                        cv2.COLOR_GRAY2BGR
                )

                cv2.polylines(
                        vis_polygon,
                        polygons,
                        True,
                        (0, 0, 255),  # red
                        2
                )

                cv2.imwrite(polygon_file, vis_polygon)





        # image_files = list(in_dir.glob(f'*_image{ext}'))

        # if not image_files:
        #         err = f"TODO2 err msg"
        #         raise Exception(err)  # TOD oexc type

        # n_total = len(list(image_files))

        # n_val = round(n_total * postconfig.additional_keys['val'])
        # n_test = round(n_total * postconfig.additional_keys['test'])

        # n_train = n_total - n_val - n_test


        # for image_file in image_files:
        #         mask_file = image_file.with_name(image_file.name.replace('image', 'mask'))  # TODO2 more elegant soln?

        #         print('hi')

        #         #shutil.copy(image_file, )






        # if image_files:
        #         print('yeet')

        # for img in image_files:
        #         print(img.stem)


# ======================================================================
# YOLO POST-PROCESSING FUNCTION
# ======================================================================


def yolo(
        in_dir:pathlib.Path,
        out_dir:pathlib.Path,
        job_input: JobInput
) -> None:
        r"""TODO docstring for function 'yolo'

        Args:
                in_dir (`pathlib.Path`):
                        Directory containg image and mask files.
                out_dir (`pathlib.Path`):
                        Output base directory.
                job_input (`JobInput`):
                        Job input.

        Raises:
                FileNotFoundError:
                        No mask file exists for an image file.
                FilenotFoundError:
                        No image-mask pairs exist in the input
                        directory.
                ValueError:
                        The sum of validation and test images specified
                        in the job input exceeds the total number of
                        image-mask pairs in the input directory.
                ValueError:
                        Invalid image file format specified in the job
                        input.
                ValueError:
                        Invalid mode specified in the job input.

        """

        # TODO refactor (incl. docstring)


        # ---- Unpack job input ----

        mode = job_input.mode
        n_val = typing.cast(
                NonNegativeInt,
                job_input.additional_keys['n_val']
        )
        n_test = typing.cast(
                NonNegativeInt,
                job_input.additional_keys['n_test']
        )
        seed = typing.cast(
                int | float | str,
                job_input.additional_keys['seed']
        )
        visualise = typing.cast(bool, job_input.additional_keys['visualise'])


        # ---- Create base output directory structure ----

        # out_dir
        # +---images
        # +---labels
        # \---visualise (if 'visualise' is 'True')

        (out_dir / 'images').mkdir()
        (out_dir / 'labels').mkdir()

        if visualise:
                visualise_dir = out_dir / 'visualise'
                visualise_dir.mkdir()
        else:
                visualise_dir = None


        # ---- Load instance-to-class mapping ----

        class_map = _load_class_map(in_dir)


        # ---- Find image-mask pairs and split into train-val-test ----

        match job_input.file_format:
                case 'jpeg':
                        ext = '.jpeg'
                case 'png':
                        ext = '.png'
                case _:
                        err = f"invalid file format: '{ext}'"
                        raise ValueError(err)

        pairs: list[tuple[pathlib.Path, pathlib.Path]] = []

        for image_file in in_dir.glob(f'*_image{ext}'):
                prefix = image_file.stem[:-6]

                mask_file = in_dir / f'{prefix}_mask.exr'

                if not mask_file.is_file():
                        err = f"no mask for image: '{mask_file.as_posix()}'"
                        raise FileNotFoundError(err)

                pairs.append((image_file, mask_file))

        n_total = len(pairs)
        n_train = n_total - n_val - n_test

        if n_total < 1:
                err = (
                        f"no image-mask pairs in directory: "
                        f"'{in_dir.as_posix()}'"
                )
                raise FileNotFoundError(err)

        if n_train < 1:
                err = (
                        f"sum of 'n_val' and 'n_test' exceeds 'n_total': "
                        f"{n_val + n_test} > {n_total}"
                )
                raise ValueError(err)

        random.seed(seed)
        random.shuffle(pairs)

        train_pairs = pairs[:n_train]
        val_pairs = pairs[n_train:n_train+n_val]
        test_pairs = pairs[n_train+n_val:]

        splits = {
                'train': train_pairs,
                'val': val_pairs,
                'test': test_pairs
        }


        # ---- Create annotations ----

        for split_name, split_pairs in splits.items():
                images_dir = out_dir / 'images' / split_name
                labels_dir = out_dir / 'labels' / split_name

                images_dir.mkdir()
                labels_dir.mkdir()

                match mode:
                        case 'yolo_box':
                                for pair in split_pairs:
                                        _yolo_box(
                                                pair,
                                                images_dir,
                                                labels_dir,
                                                visualise_dir,
                                                job_input,
                                                class_map
                                        )
                        case 'yolo_poly':
                                for pair in split_pairs:
                                        _yolo_poly(
                                                pair,
                                                images_dir,
                                                labels_dir,
                                                visualise_dir,
                                                job_input,
                                                class_map
                                        )
                        case _:
                                err = f"invalid mode: '{mode}'"
                                raise ValueError(err)


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['yolo']


#<file:end>

