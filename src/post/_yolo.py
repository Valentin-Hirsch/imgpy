# src/post/_yolo.py
"""Post-processing of rendered images for YOLO datasets.

This module provides the :func:`yolo` function.

"""


# ======================================================================
# IMPORTS
# ======================================================================

import pathlib
import random
import shutil
import typing

import cv2
import numpy as np

from .models import JobInput
from src.common import NonNegativeInt, PositiveInt


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def _yolo_box(
        pair: tuple[pathlib.Path, pathlib.Path],
        images_dir: pathlib.Path,
        labels_dir: pathlib.Path,
        visualise_dir: pathlib.Path | None,
        postconfig: JobInput
) -> None:
        r"""TODO docstring

        TODO

        Arguments:
                pair (tuple[pathlib.Path, pathlib.Path]):
                        TODO
                images_dir (pathlib.Path):
                        TODO
                labels_dir (pathlib.Path):
                        TODO
                visualise_dir (pathlib.Path | None):
                        TODO
                postconfig (PostConfig):
                        TODO

        Raises:
                FileNotFoundError:
                        Failed to read mask file.

        """

        # TODO refactor (incl. docstring)


        # ---- Unpack arguments and job input ----

        image_file = pair[0]
        mask_file = pair[1]

        class_id = postconfig.class_id
        create_empty = typing.cast(
                bool,
                postconfig.additional_keys['create_empty']
        )
        threshold = typing.cast(
                PositiveInt,
                postconfig.additional_keys['threshold']
        )


        # ---- Copy image file ----

        shutil.copy2(image_file, images_dir / image_file.name)


        # ---- Create label file ----

        label_file = labels_dir / f'{image_file.stem}.txt'

        mask = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)

        # 'mask' is a 2D NumPy array:
        #
        # mask = [
        #         [uint8, ...], -> line of the image
        #         ...
        # ]

        if mask is None:
                err = f"failed to read mask: '{mask_file.as_posix()}'"
                raise FileNotFoundError(err)

        mask = (mask >= threshold).astype(np.uint8)

        if not np.any(mask):
                if create_empty:
                        with label_file.open(mode='x', encoding='utf-8') as fp:
                                fp.write('\n')

                return

        shape: tuple[int, int] = mask.shape
        height = shape[0]
        width = shape[1]

        ys, xs = np.nonzero(mask)

        x_min = int(xs.min())
        x_max = int(xs.max())
        y_min = int(ys.min())
        y_max = int(ys.max())

        annotation = (
                f'{class_id} '
                f'{(x_min + x_max + 1) / (2 * width):.6f} '
                f'{(y_min + y_max + 1) / (2 * height):.6f} '
                f'{(x_max - x_min + 1) / width:.6f} '
                f'{(y_max - y_min + 1) / height:.6f}\n'
        )

        with label_file.open(mode='x', encoding='utf-8') as fp:
                fp.write(annotation)


        # ---- Visualisation ----

        if visualise_dir is not None:
                visualise_file = visualise_dir / f'{mask_file.stem}_box.png'

                visualisation = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR)

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
        postconfig: JobInput
) -> None:
        r"""TODO docstring"""

        # TODO refactor (incl. docstring)

        # ---- Unpack arguments and job input ----

        image_file = pair[0]
        mask_file = pair[1]

        class_id = postconfig.class_id
        create_empty = typing.cast(
                bool,
                postconfig.additional_keys['create_empty']
        )
        simplify = typing.cast(float, postconfig.additional_keys['simplify'])  # TODO PositiveFloat?
        threshold = typing.cast(
                PositiveInt,
                postconfig.additional_keys['threshold']
        )


        # ---- Copy image file ----

        shutil.copy2(image_file, images_dir / image_file.name)


        # ---- Create label file ----

        label_file = labels_dir / f'{image_file.stem}.txt'

        mask = cv2.imread(mask_file, cv2.IMREAD_GRAYSCALE)

        # 'mask' is a 2D NumPy array:
        #
        # mask = [
        #         [uint8, ...], -> line of the image
        #         ...
        # ]

        if mask is None:
                err = f"failed to read mask: '{mask_file.as_posix()}'"
                raise FileNotFoundError(err)

        mask = (mask >= threshold).astype(np.uint8)

        if not np.any(mask):
                if create_empty:
                        with label_file.open(mode='x', encoding='utf-8') as fp:
                                fp.write('\n')

                return

        shape: tuple[int, int] = mask.shape
        height = shape[0]
        width = shape[1]

        work = mask.copy()

        while True:
                contours, _ = cv2.findContours(
                        work,
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_NONE
                )

                if len(contours) <= 1:
                        break

                best_distance = np.inf
                best_pair = None

                # TODO whole block....
                for i in range(len(contours)):
                        a = contours[i][:, 0, :]

                        for j in range(i+1, len(contours)):
                                b = contours[j][:, 0, :]

                                diff = a[:, None] - b[None]
                                distances = np.sum(diff * diff, axis=2)

                                ia, ib = np.unravel_index(np.argmin(distances), distances.shape)

                                if distances[ia, ib] < best_distance:
                                        best_distance = distances[ia, ib]
                                        best_pair = (a[ia], b[ib])

                p1, p2 = best_pair
                cv2.line(work, tuple(p1), tuple(p2), 1, 1)

        contours, _ = cv2.findContours(
                work,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_NONE,
        )

        contour = contours[0]

        epsilon = simplify * cv2.arcLength(contour, True)
        contour = cv2.approxPolyDP(contour, epsilon, True)

        coords: list[str] = []

        for x, y in contour[:, 0]:
                coords.append(f'{x / width:.6f}')
                coords.append(f'{y / height:.6f}')

        annotation = f'{class_id} ' + ' '.join(coords) + '\n'

        with label_file.open(mode='x', encoding='utf-8') as fp:
                fp.write(annotation)


        # ---- Visualisation ----

        if visualise_dir is not None:
                bridges_file = visualise_dir / f'{mask_file.stem}_bridges.png'
                polygon_file = visualise_dir / f'{mask_file.stem}_polygon.png'

                vis_bridges = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR)
                vis_polygon = cv2.cvtColor(mask * 255, cv2.COLOR_GRAY2BGR)

                bridges = (work == 1) & (mask == 0)
                vis_bridges[bridges] = [255, 255, 0]  # cyan

                cv2.polylines(
                        vis_polygon,
                        [contour],
                        True,
                        (0, 0, 255),  # red
                        2
                )

                cv2.imwrite(bridges_file, vis_bridges)
                cv2.imwrite(polygon_file, vis_polygon)





        # image_files = list(in_dir.glob(f'*_image{ext}'))

        # if not image_files:
        #         err = f"TODO err msg"
        #         raise Exception(err)  # TOD oexc type

        # n_total = len(list(image_files))

        # n_val = round(n_total * postconfig.additional_keys['val'])
        # n_test = round(n_total * postconfig.additional_keys['test'])

        # n_train = n_total - n_val - n_test


        # for image_file in image_files:
        #         mask_file = image_file.with_name(image_file.name.replace('image', 'mask'))  # TODO more elegant soln?

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
        r"""TODO docstring

        TODO

        Arguments:
                in_dir (pathlib.Path):
                        Directory containg image and mask files.
                out_dir (pathlib.Path):
                        Output base directory.
                postconfig (PostConfig):
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

                mask_file = in_dir / f'{prefix}_mask.png'

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
                                                job_input
                                        )
                        case 'yolo_poly':
                                for pair in split_pairs:
                                        _yolo_poly(
                                                pair,
                                                images_dir,
                                                labels_dir,
                                                visualise_dir,
                                                job_input
                                        )
                        case _:
                                err = f"invalid mode: '{mode}'"
                                raise ValueError(err)


# ======================================================================
# INTERNAL EXPORT
# ======================================================================

__all__ = ['yolo']


#<file:end>

