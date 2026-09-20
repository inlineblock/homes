# Rebuilding Twin Gables Courtyard

Run from the repository root with Blender 4.5 LTS and Python 3.11 or later. The checked-in native file uses relative library links; clone with Git LFS before opening it. Keep `homes/` and `library/` together.

IFC export also requires an IfcOpenShell runtime compatible with Blender's Python and the installed Bonsai extension. If it is not on Blender's import path, pass `-- --runtime-path /path/to/compatible/site-packages` to `export_ifc.py`; that path is a local runtime prerequisite, not an architectural asset dependency.

`tools/twin_gables/design.py` owns the floorplate, room coordinates, roof datums and cameras. The authoring code takes feet-based planning dimensions and builds in meters. `model/plan-data.json` records actual modeled placements for the furnished drawings. Change the model and drawings together.

```sh
blender --factory-startup --background --python-exit-code 1 --python tools/twin_gables/build.py
blender --factory-startup --background homes/eichler-twin-gables/model/eichler-twin-gables.blend --python-exit-code 1 --python tools/twin_gables/verify.py
blender --factory-startup --background homes/eichler-twin-gables/model/eichler-twin-gables.blend --python-exit-code 1 --python tools/twin_gables/verify_function.py
blender --factory-startup --background homes/eichler-twin-gables/model/eichler-twin-gables.blend --python-exit-code 1 --python tools/twin_gables/render.py -- --width 2000 --samples 256
python3 tools/twin_gables/draw_plan.py
blender --factory-startup --background homes/eichler-twin-gables/model/eichler-twin-gables.blend --python-exit-code 1 --python tools/twin_gables/export_ifc.py
blender --background --python-exit-code 1 --python tools/twin_gables/verify_bonsai.py
blender --factory-startup --background --python-exit-code 1 --python tools/common/verify_repository.py -- --homes eichler-twin-gables
```

On macOS, the Blender executable is normally inside `Blender.app/Contents/MacOS/`. Use the installed executable in place of `blender` when it is not on your command path. Coordinate GPU use with other active renders.

The build replaces this home's native file and derived model records. Render and plan candidates go to ignored `outputs/work/`; inspect their actual pixels before promoting them into `outputs/images/` and `outputs/plans/`. Never save a cutaway or temporary render state over the furnished native model.

After the native views pass review, use the built-in ImageGen editing tool with each actual render as its reference. Preserve geometry, viewpoint and equipment; record the exact prompt, source hash and selected image hash in `outputs/photo-provenance.json`. Photographic studies are interpretations, not evidence that an unmodeled feature exists. The local output-review skill describes the full workflow.

After the model, IFC, plans and photographic studies are reviewed, publish the gallery and refresh the compact root directory:

```sh
python3 tools/twin_gables/publish_gallery.py --review-note "Describe the actual completed visual review here."
python3 tools/common/write_catalog.py
python3 tools/common/verify_galleries.py
```

Do not copy the example review note as a completed check. Update `project.json`, the asset schedule and design review with the actual final dependencies and evidence. Stable output filenames hold the current reviewed result; Git retains history.
