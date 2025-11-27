# Mesher







from pathlib import Path
from typing import Any
import argparse
import cadquery as cq
import gmsh  # TODO error: figure out or ignore
import json
import logging
import sys
import time






def cadquery_mesh(mesh_settings: dict[str, dict[str, Any]]) -> None:
  r"""TODO docstring
  
  - START_TS
  - IN_FPATH
  - OUT_DPATH

  """
  
  part = cq.importers.importStep(STEP_FPATH.as_posix())

  out_fname = f"{START_TS}-cadquery-{STEP_FPATH.stem}.3mf"
  out_fpath = Path(OUT_DPATH, out_fname)

  part.export(
    out_fpath.as_posix(),
    tolerance=mesh_settings["3mf"]["tolerance"],
    angularTolerance=mesh_settings["3mf"]["angularTolerance"]
  )





def gmsh_mesh(mesh_settings: dict[str, dict[str, Any]]) -> None:
  r"""TODO docstring
  
  needs:
  
  - START_TS
  - IN_FPATH
  - OUT_DPATH

  """
  
  gmsh.initialize()

  gmsh.option.setNumber("General.Terminal", 1)

  gmsh.model.add("part")
  gmsh.model.occ.importShapes(STEP_FPATH.as_posix())
  gmsh.model.occ.synchronize()

  gmsh.model.mesh.generate(2)

  out_fname = f"{START_TS}-gmsh-{STEP_FPATH.stem}.stl"
  out_fpath = Path(OUT_DPATH, out_fname)

  gmsh.write(out_fpath.as_posix())

  gmsh.finalize()











if __name__ == "__main__":
  START_TS = time.strftime(r"%Y%m%d-%H%M%S")
  SCRIPT_DPATH = Path(__file__).resolve().parent  # 'src' directory
  BASE_DPATH = SCRIPT_DPATH.parent  # 'semester-project' directory
  OUT_DPATH = Path(BASE_DPATH, "output")  # 'output' directory

  #region ARGUMENT HANDLING

  parser = argparse.ArgumentParser()

  parser.add_argument(
    "-f",
    "--file",
    help="TODO help for file argument",
    type=Path,
    default=Path(BASE_DPATH, "data", "geom", "nut.step")
  )
  parser.add_argument(
    "-l",
    "--log",
    help="TODO help for log argument",
    action="store_true"
  )

  parser.add_argument(
    "-m",
    "--mesher",
    help="TODO help for mesher argument",
    choices=["cadquery", "gmsh"],
    default="cadquery"
  )

  args = parser.parse_args()

  STEP_FPATH: Path = args.file.resolve()
  TO_FILE: bool = args.log
  MESHER: str = args.mesher

  #endregion

  #region LOGGER SET-UP

  logger = logging.getLogger(__name__)
  logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt=r"%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
  )

  #endregion



 

  if (
    not STEP_FPATH.is_file()
    or STEP_FPATH.suffix.lower() != ".step"
  ):
    err = f"TODO error input file not file or not STEP file: '{STEP_FPATH}'"
    logger.error(err)
    raise Exception(err)








  #region MESHING AND OUTPUT

  fpath = Path(BASE_DPATH, "data", "settings","mesh-settings.json")
  with fpath.open(mode="r", encoding="utf-8") as file:
    mesh_settings: dict[str, dict[str, dict[str, Any]]] = json.load(file)

  match MESHER:
    case "cadquery":
      cadquery_mesh(mesh_settings["cadquery"])
    case "gmsh":
      gmsh_mesh(mesh_settings["gmsh"])
    case _:
      err = f"TODO error unknown mesher"
      logger.error(err)
      raise Exception(err)

  #endregion

  sys.exit("fin.")



















  logger.info(f"log is {args.log}")



  nut = cq.importers.importStep(args.file.as_posix())
  nut.export(f"{START_TS}-nut.STL")































#<file:end>
