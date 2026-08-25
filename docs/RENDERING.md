# Rendering synthetic images

This guide covers the `render` and `post` steps of the ImgPy pipeline:
generating photorealistic images of a part in a scene via Blender/Cycles,
and turning the rendered image + mask pairs into a YOLO dataset.

For CAD meshing (`mesh` mode) see `src/mesh`.

## Pipeline

```
render job JSON --> src.imgpy.render_images --> workdir/<job>/render/*_image.<ext>
                                                  workdir/<job>/render/*_mask.exr
                                                  workdir/<job>/render/classes.json

post job JSON   --> src.post.post_process     --> out_dir/images/{train,val,test}
                                                  out_dir/labels/{train,val,test}
```

```
python -m src render -i workdir/render.json [-j workdir/<job_dir>]
python -m src post   -i workdir/post.json    [-o workdir/<out_dir>]
```

Each render job produces, per requested image, one RGB image and one EXR
object-index mask with the same numeric prefix (`0_image.png`,
`0_mask.exr`, ...), plus a single `classes.json` shared by the whole job
(see [Object classes & instance masks](#object-classes--instance-masks)).
The `post` job is a separate step, run only against that `render/`
directory — it does not re-open Blender.

## Render job JSON

A render job (e.g. `workdir/plumbers_block_screws_only.json`) has four
top-level sections:

- **`lens`** — a `PrimeLens` (fixed `focal_length`, `f_stop_min`/`f_stop_max`)
  or `ZoomLens` (`focal_length_wide`/`focal_length_tele` with separate
  f-stop ranges at each end). One `(focal_length, f_stop)` pair is sampled
  per rendered image and applied to the camera's depth of field.
- **`protagonist`** — the one part the dataset is "about". `file` is a
  path (relative to the job JSON) to an `.stl` or `.blend`; `class_id` is
  its YOLO class; `additional_keys` carries `material` (see
  [Materials](#materials)), `scale_factor` (STL import scale, e.g.
  `0.001` for a part modelled in millimetres), `decimate_ratio` (mesh
  decimation, `1.0` = no decimation) and `shade_mode`
  (`smooth`/`auto_smooth`/`flat`).
- **`scene`** — `name` selects a scene from `data/blender/scenes/<name>/`
  (see [Scenes, camera & lighting](#scenes-camera--lighting)), plus a
  `clutter` list of extra objects rendered alongside the protagonist
  (see [Part type & clutter](#part-type--clutter)).
- **`render`** — `resolution`, `image_count`, `file_format`
  (`png`/`jpeg`), `device_type` (`cpu`/`cuda`/`optix`/`hip`), and
  `additional_keys` (`png_compression` or `jpeg_quality` depending on
  `file_format`; `threads`, only used for `device_type: "cpu"`, `0` =
  auto).

See `data/blender/scenes/dining_table/dining_table.json` and the example
`workdir/plumbers_block_*.json` files for complete, working configs.

## Part type & clutter

The **protagonist** is the single labelled part every image is composed
around; the camera is always aimed at it (see
[Camera, world & table frames](#camera-world--table-frames)).

`scene.clutter` is a list of *additional* part types rendered alongside
it — other real parts to label, or unlabelled distractors:

```json
{
  "count": 2,
  "object": "plumbers_block_1",
  "class_id": 2,
  "material": "plastic_red",
  "scale_factor": 0.001,
  "decimate_ratio": 1.0,
  "shade_mode": "auto_smooth",
  "rigid_body": { "collision_shape": "convex_hull", "friction": 0.9, "mass": 0.05, "restitution": 0.01 }
}
```

- `object` names an STL under `data/geometry/clutter/<object>.stl` (no
  path, no extension).
- `count` instantiates that many independent copies of it, each dropped
  and settled separately by the rigid-body simulation — e.g. `count: 2`
  for a part with two identical screws.
- `class_id` is the YOLO class written for every instance. Set it to
  `null` to render the object as background clutter that is *not*
  labelled (mask pixel value `0`, never boxed/polygoned by `post`).
  Several clutter entries (and the protagonist) may share the same
  `class_id` — e.g. two different STL variants that are both "screw".

Every physical object instance gets its own **unique** mask pixel value,
regardless of how many entries or instances share a `class_id` — see
next section.

## Object classes & instance masks

The mask pass is Blender's per-object "Object Index" (`pass_index`)
compositor pass (`data/blender/common/compositing.blend`: `render_layers`
→ `file_output`), written straight to the EXR with no extra processing —
so whatever integer each Blender object is assigned is exactly the pixel
value written under it.

Previously, `pass_index` was set to `class_id + 1` directly. That is
fine for *semantic* segmentation, but **broke instance separation**:
every instance of the same clutter entry (`obj.copy()` inherits the
original's `pass_index`) — and the protagonist whenever it shared a
`class_id` with a clutter entry — painted the exact same pixel value.
`src/post/_yolo.py` recovers instances by running
`cv2.connectedComponentsWithStats` per pixel value, so two same-class
objects only became separate instances if they happened not to touch in
the 2D projection. Two screws from the same "screw" clutter entry
(`count: 2`) sitting next to each other on the table were reliably
merged into one blob — one bounding box/polygon.

**Fix:** every physical object instance (the protagonist, and each
clutter object/copy with `class_id` set) is now assigned its own
globally unique `pass_index` via `FileContext.register_instance()`
(`src/imgpy/blender/_filecontext.py`), instead of reusing `class_id + 1`.
Pixel value `0` is still reserved for background/unlabelled objects
(`class_id: null`). The `{pass_index: class_id}` mapping is written once
per job to `<job_dir>/render/classes.json` right after scene set-up
(`src/imgpy/_core.py`).

`src/post/_yolo.py` loads that file and groups mask pixels by the raw
instance value (looking up `class_id` through the map) instead of
deriving the class from the pixel value directly. Because every instance
now has a distinct value, touching/overlapping objects of the same class
are always separate connected components — including the two-screw case
above — with no dependency on them being spatially disjoint in the
rendered image.

`classes.json` lives next to the masks it describes and is required by
`post`; a `render/` directory produced before this change (no
`classes.json`) cannot be post-processed.

## Materials

`material` (protagonist `additional_keys.material`, or a clutter entry's
`material`) names a `.blend` file under `data/blender/materials/`
(`plastic_yellow`, `plastic_red`, `brass_v1`/`v2`, `metal_brushed_v1`/
`v2`, `metal_anodised_blue_v1`/`v2`, `metal_black_oxide_v1`/`v2`,
`metal_smooth_v1`/`v2`, `wood_plank_v1`/`v2`, `plaster_v1`/`v2`,
`concrete`, ...). The named material is imported into the working
`.blend` on first use and reused for any later object in the same job
that references the same name — different objects can share a material
without re-importing it.

## Scenes, camera & lighting

A scene under `data/blender/scenes/<name>/` bundles three files, all
selected by `scene.name` in the render job:

- `<name>.blend` — the world itself: room geometry (floor/walls/
  ceiling), a `table`-like surface, lights, and the camera. This is what
  currently determines the **background** — there is no per-job
  background swap; changing background means picking a different scene
  (or adding a new one).
- `<name>.py` — `SceneConfig` (the scene's own config schema) plus
  `set_up()`/`randomise()`, which place the protagonist/clutter,
  randomise the camera and lights, and (re-)bake the rigid-body physics
  simulation so parts settle naturally on the table.
- `<name>.json` — values for that `SceneConfig`: camera
  `location_range`, clutter `initial_location_range`, protagonist
  `initial_location`, per-light `location_range`/`power_range`/
  `temperature_range`, and rigid-body simulation `frame_start`/
  `frame_end`.

Two scenes ship today: `dining_table` (table surface around world
`z ≈ 0.9–1.0`) and `robot_table` (table surface around world
`z ≈ 1.2–1.5`) — location ranges in a scene's JSON are only meaningful
relative to that scene's own table height.

`job_input.scene.additional_keys.reset` controls how often (in images)
the scene is fully re-randomised and re-simulated versus just moving the
camera/lights for a new shot of the same settled arrangement — e.g.
`"reset": 5` re-drops the parts every 5th image.

### Camera, world & table frames

There is a single coordinate system per scene — Blender's scene "world"
space — shared by the table/room geometry, lights, camera and every
placed part. There is no separate table-local frame: the table's top
surface is simply modelled at a fixed world-space height (see the two
scenes' `z` ranges above), and every `location_range`/
`initial_location` in a scene's JSON is an absolute world-space
coordinate that must sit at/above that height to land on the table.

Camera **position** is re-sampled every image from
`scene.render.camera.location_range`, an absolute world-space box (set
once per scene to frame that scene's table). Camera **orientation** is
never set directly by config: a `TRACK_TO` constraint, created once
during set-up and targeting the protagonist's origin, continuously
re-aims the camera's local `-Z` axis at the protagonist (Blender's
default `track_axis`/`up_axis` for this constraint, `TRACK_NEGATIVE_Z`/
`UP_Y`, are unchanged), and `camera.data.dof.focus_object` is likewise
the protagonist. In effect: place the camera anywhere in world space
inside the scene's `location_range`, and it always frames and focuses on
the protagonist automatically — accurate framing is a matter of keeping
that box at a distance/angle from the table that the sampled lens's
focal length can actually cover, not of computing any camera-to-table
transform by hand.

## Post-processing job JSON

```json
{
  "job_name": "plumbers_block_screws_only",
  "directory": "20260817-145547-render-plumbers_block_screws_only/render",
  "file_format": "png",
  "mode": "yolo_box",
  "additional_keys": {
    "create_empty": false,
    "min_component_area": 25,
    "n_val": 2,
    "n_test": 2,
    "seed": 0,
    "visualise": true
  }
}
```

- `directory` is the render job's `render/` output, relative to this
  JSON's own location.
- `mode`: `yolo_box` (axis-aligned boxes) or `yolo_poly` (polygons; add
  `additional_keys.simplify`, the `cv2.approxPolyDP` epsilon fraction of
  contour length).
- `min_component_area` drops connected-component noise (anti-aliased
  mask edges) below that pixel area.
- `n_val`/`n_test` images are split off (by `seed`) into `val`/`test`;
  everything else becomes `train`.
- `create_empty` writes an empty label file for images with no
  surviving annotation instead of skipping them; `visualise` additionally
  writes annotated preview images to `out_dir/visualise/`.
