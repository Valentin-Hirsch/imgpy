# src/__main__.py
r"""Command-line entry point.

This module provides the toolkit's command line interface. It parses
command-line arguments and dispatches execution to the selected mode.

The following modes are available:

- `mesh`
- `post`
- `render`

"""


# ======================================================================
# IMPORTS
# ======================================================================

import argparse
import logging
import pathlib
import sys

import src.imgpy
import src.mesh
import src.post


# ======================================================================
# CONSTANTS
# ======================================================================

LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
}


# ======================================================================
# HELPER FUNCTIONS
# ======================================================================


def parse_args() -> argparse.Namespace:
        r"""Parse command-line arguments.

        Returns:
                `argparse.Namespace`:
                        Namespace of command-line arguments.

        """

        parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=(
                        "ImgPy - A Procedural Toolkit for Synthetic Computer "
                        "Vision Dataset Generation"
                ),
                epilog=(
                        "Usage examples:\n"
                        "  %(prog)s mesh -i workdir/object.step\n"
                        "  %(prog)s post -i workdir/post.json\n"
                        "  %(prog)s render -i workdir/render.json"
                )
        )
        parser.add_argument(
                '-d',
                '--data_dir',
                help="Data directory (default: None).",
                required=False,
                type=pathlib.Path,
                default=None
        )
        parser.add_argument(
                '-l',
                '--log_lvl',
                help="Logging level (default: 'info').",
                required=False,
                type=str,
                default='info',
                choices=LOG_LEVELS.keys()
        )
        parser.add_argument(
                '-w',
                '--work_dir',
                help="Working directory (default: None).",
                required=False,
                type=pathlib.Path,
                default=None
        )

        subparsers = parser.add_subparsers(
                title='mode',
                dest='mode',
                required=True,
                description="ImgPy mode."
        )


        # --------------------------------------------------------------
        # MODE MESH
        # --------------------------------------------------------------

        ps_mesh = subparsers.add_parser(
                'mesh',
                formatter_class=argparse.RawTextHelpFormatter,
                description="Mesh a CAD file to an output file.",
                epilog=(
                        "Usage examples:\n"
                        "  %(prog)s -i workdir/object.step\n"
                        "  %(prog)s -i workdir/object.step -m gmsh -o "
                        "workdir/object.stl"
                )
        )
        ps_mesh.add_argument(
                '-i',
                '--in_file',
                help="CAD file.",
                required=True,
                type=pathlib.Path
        )
        ps_mesh.add_argument(
                '-m',
                '--mesh_engine',
                help="Meshing engine (default: 'cadquery').",
                required=False,
                type=str,
                choices=src.mesh.MESH_ENGINES,
                default='cadquery'
        )
        ps_mesh.add_argument(
                '-o',
                '--out_file',
                help="Output file. If omitted, defaults to STL.",
                required=False,
                type=pathlib.Path,
                default=None
        )


        # --------------------------------------------------------------
        # MODE POST
        # --------------------------------------------------------------

        ps_post = subparsers.add_parser(
                'post',
                formatter_class=argparse.RawTextHelpFormatter,
                description="Run a post-processing job.",
                epilog=(
                        "Usage examples:\n"
                        "  %(prog)s -i workdir/post.json\n"
                        "  %(prog)s -i workdir/post.json -o workdir/post"
                )
        )
        ps_post.add_argument(
                '-i',
                '--in_file',
                help="Input file.",
                required=True,
                type=pathlib.Path
        )
        ps_post.add_argument(
                '-o',
                '--out_dir',
                help="Output directory.",
                required=False,
                type=pathlib.Path,
                default=None
        )


        # --------------------------------------------------------------
        # MODE RENDER
        # --------------------------------------------------------------

        ps_render = subparsers.add_parser(
                'render',
                formatter_class=argparse.RawTextHelpFormatter,
                description="Run an image rendering job.",
                epilog=(
                        "Usage examples:\n"
                        "  %(prog)s -i workdir/render.json\n"
                        "  %(prog)s -i workdir/render.json -j workdir/render"
                )
        )
        ps_render.add_argument(
                '-i',
                '--in_file',
                help="Input file.",
                required=True,
                type=pathlib.Path
        )
        ps_render.add_argument(
                '-j',
                '--job_dir',
                help="Job directory.",
                required=False,
                type=pathlib.Path,
                default=None
        )

        return parser.parse_args()


# ======================================================================
# MAIN FUNCTION
# ======================================================================


def main() -> None:
        r"""Main function."""

        args = parse_args()

        log_level: str = args.log_lvl

        logger = logging.getLogger(__name__)
        logging.basicConfig(
                format='[%(asctime)s] [%(levelname)s] %(message)s',
                datefmt=r'%Y-%m-%d %H:%M:%S',
                level=LOG_LEVELS[log_level]
        )

        data_dir: pathlib.Path | None = args.data_dir
        work_dir: pathlib.Path | None = args.work_dir

        if data_dir is not None:
                src.imgpy.config.data_dir = data_dir
                src.mesh.config.data_dir = data_dir
                src.post.config.data_dir = data_dir

        if work_dir is not None:
                src.imgpy.config.work_dir = work_dir
                src.mesh.config.work_dir = work_dir
                src.post.config.work_dir = work_dir

        mode: str = args.mode

        try:
                match mode:
                        case 'mesh':
                                src.mesh.mesh_file(
                                        args.in_file,
                                        mesh_engine=args.mesh_engine,
                                        out_file=args.out_file
                                )
                        case 'post':
                                src.post.post_process(
                                        args.in_file,
                                        out_dir=args.out_dir
                                )
                        case 'render':
                                src.imgpy.render_images(
                                        args.in_file,
                                        job_dir=args.job_dir
                                )
                        case _:
                                err = f"invalid mode '{mode}'"
                                raise ValueError(err)
        # TODO catch specific excs
        except Exception as e:
                msg = f"Uncaught exception in main: {e}"
                logger.critical(msg, exc_info=True)
                sys.exit(1)


# ======================================================================
# RUN
# ======================================================================

if __name__ == '__main__':
        main()


# ======================================================================
# PUBLIC API
# ======================================================================

__all__ = []


#<file:end>
