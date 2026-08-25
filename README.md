# ImgPy - Synthetic Dataset Generation Pipeline

A procedural toolkit for generating photorealistic synthetic images and YOLO datasets from CAD models. ImgPy orchestrates a three-stage pipeline: **mesh** (convert CAD to STL), **render** (place objects in scenes via Blender), and **post** (extract YOLO annotations).

## Quick Start

### 1. Install & Setup

```bash
pip install -r requirements.txt
```

### 2. Render Images (Typical Workflow)

The most common workflow is rendering images from an STL file:

```bash
# Create a render job JSON (see workdir/plumbers_block_*.json for examples)
python -m src render -i workdir/render.json
```

**Output:** Images and masks in `workdir/<job>/render/`

### 3. Post-Process to YOLO Dataset

```bash
python -m src post -i workdir/post.json [-o output_dir]
```

**Output:** YOLO-formatted train/val/test splits in `output_dir/images/` and `output_dir/labels/`

---

## Pipeline Stages

### Stage 1: Mesh (Optional)

Convert CAD geometry (STEP files) to STL for rendering:

```bash
python -m src mesh -i object.step [-m cadquery|gmsh] [-o object.stl]
```

- **Default engine:** CadQuery (faster for simple models)
- **Alternative:** Gmsh (more control, better for complex geometry)

### Stage 2: Render

Generate RGB images and instance masks in Blender:

```bash
python -m src render -i workdir/render.json [-j workdir/jobs]
```

**Outputs per image:**
- `N_image.png` — RGB image
- `N_mask.exr` — Object instance mask (per-object unique IDs)
- `classes.json` — Class ID mapping (per job)

### Stage 3: Post-Process

Convert rendered masks to YOLO bounding boxes or polygons:

```bash
python -m src post -i workdir/post.json [-o output_dir]
```

**Outputs:**
- `images/{train,val,test}/*.png` — Images
- `labels/{train,val,test}/*.txt` — YOLO format annotations

---

## Important Parameters

### Render Job JSON (`render.json`)

Create a JSON file following the structure in `workdir/plumbers_block_*.json`:

#### **`lens`** — Camera optics
- `PrimeLens`: Fixed focal length with depth-of-field range
  ```json
  "lens": {"type": "PrimeLens", "focal_length": 50, "f_stop_min": 1.0, "f_stop_max": 5.0}
  ```
- `ZoomLens`: Telephoto/wide variation per image
  ```json
  "lens": {"type": "ZoomLens", "focal_length_wide": 28, "focal_length_tele": 85, ...}
  ```

#### **`protagonist`** — The labeled object (YOLO class)
```json
"protagonist": {
  "file": "path/to/model.stl",
  "class_id": 1,
  "additional_keys": {
    "material": "plastic_yellow",        // ← material name (no .blend extension)
    "scale_factor": 0.001,               // ← STL to world scale (mm → m: 0.001)
    "decimate_ratio": 1.0,               // ← mesh decimation (1.0 = no reduction)
    "shade_mode": "smooth"               // ← smooth, auto_smooth, or flat
  }
}
```

**Key materials:** `plastic_yellow`, `plastic_red`, `brass_v1`, `brass_v2`, `metal_brushed_v1`, `metal_smooth_v1`, `wood_plank_v1`, etc.

#### **`scene`** — Environment & setup
```json
"scene": {
  "name": "dining_table",              // ← scene preset (dining_table, robot_table)
  "additional_keys": {
    "reset": 5                           // ← re-randomize every N images
  },
  "clutter": [                           // ← background/extra objects
    {
      "object": "plumbers_block_1",
      "count": 2,
      "class_id": 2,
      "material": "plastic_red",
      "scale_factor": 0.001,
      "shade_mode": "auto_smooth"
      // "class_id": null for unlabeled distractors
    }
  ]
}
```

**Available scenes:**
- `dining_table` — typical worktable, table height ~0.9–1.0m
- `robot_table` — raised work surface, table height ~1.2–1.5m

#### **`render`** — Image generation settings
```json
"render": {
  "resolution": [1024, 1024],
  "image_count": 50,
  "file_format": "png",                 // ← png or jpeg
  "device_type": "cuda",                // ← cpu, cuda, optix, hip
  "additional_keys": {
    "png_compression": 9,               // ← 0–9 (if format: png)
    "threads": 0                        // ← 0 = auto (if device: cpu)
  }
}
```

### Post-Job JSON (`post.json`)

```json
{
  "job_name": "my_dataset",
  "directory": "20260817-145547-render-job/render",  // ← path to render output
  "file_format": "png",
  "mode": "yolo_box",                   // ← yolo_box or yolo_poly
  "additional_keys": {
    "min_component_area": 25,           // ← drop masks smaller than N pixels
    "n_val": 2,                         // ← number of validation images
    "n_test": 2,                        // ← number of test images
    "seed": 42,                         // ← reproducibility
    "visualise": true                   // ← generate annotated preview images
  }
}
```

---

## File Structure

```
imgpy/
├── data/
│   ├── blender/
│   │   ├── materials/          # .blend material libraries
│   │   ├── scenes/             # .blend scene environments + Python configs
│   │   └── common/             # shared Blender utilities
│   └── geometry/
│       ├── protagonist/        # main object STLs
│       └── clutter/            # secondary object STLs
├── src/
│   ├── imgpy/                  # render engine
│   ├── mesh/                   # CAD-to-STL conversion
│   ├── post/                   # YOLO post-processing
│   └── common/                 # utilities
├── workdir/                    # job configs & outputs
└── docs/
    └── RENDERING.md            # detailed rendering guide
```

---

## Complete Example

1. **Create render job** (`workdir/my_render.json`):
```json
{
  "lens": {"type": "PrimeLens", "focal_length": 50, "f_stop_min": 2.0, "f_stop_max": 5.0},
  "protagonist": {
    "file": "data/geometry/protagonist/part.stl",
    "class_id": 1,
    "additional_keys": {
      "material": "plastic_yellow",
      "scale_factor": 0.001,
      "decimate_ratio": 1.0,
      "shade_mode": "smooth"
    }
  },
  "scene": {"name": "dining_table", "additional_keys": {"reset": 5}, "clutter": []},
  "render": {
    "resolution": [1024, 1024],
    "image_count": 100,
    "file_format": "png",
    "device_type": "cuda",
    "additional_keys": {"png_compression": 9}
  }
}
```

2. **Render images:**
```bash
python -m src render -i workdir/my_render.json
```

3. **Create post job** (`workdir/my_post.json`):
```json
{
  "job_name": "my_dataset",
  "directory": "20260825-143022-render-my_render/render",
  "file_format": "png",
  "mode": "yolo_box",
  "additional_keys": {
    "min_component_area": 25,
    "n_val": 10,
    "n_test": 10,
    "seed": 42,
    "visualise": true
  }
}
```

4. **Post-process:**
```bash
python -m src post -i workdir/my_post.json -o workdir/my_dataset
```

---

## Advanced Topics

See `docs/RENDERING.md` for:
- Detailed camera positioning and rigid-body physics
- Object instance masking & class ID mapping
- Multi-class YOLO mask support
- Scene customization & animation







## Links

- [`nut.STEP`](https://www.mcmaster.com/94223A105/)
- [Material Pack Wood - 03](https://juliosillet.gumroad.com/l/Dvdll)





## Notes








`<file:end>`
