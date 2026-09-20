# Atrium 01 generation

- `design.py` owns the measured layout in meters. `architecture.py` builds enclosure/site/supports; `interiors.py` and `kitchen.py` place furnishings and equipment; `shading.py` pairs bedroom shade states. `cameras.py` owns framing. Shared primitives belong in `tools/common/`.
- `build.py` overwrites the native model, project manifest, design metadata and `interiors-layout.json`. Preserve manual edits first. It links exact library versions, cuts actual fixture/roof openings, maps timber grain and saves relative paths. Do not save temporary render or IFC states over that file.
- Maintain 2,400 sq ft gross enclosed, the open-air courtyard, three bedrooms/baths, enclosed circulation, sheltered arrival and walnut/sage kitchen. Finished ceiling is 10 ft 6 in, main beam clearance 9 ft 6 in and service ceiling 9 ft; coordinate fixtures and glazing with actual obstructions.
- Fresh `verify.py` checks evaluated linked meshes, equipment/cabinet operation, moving doors/sliders, indoor routes, storage, fixture heights, parking, glazing and both shade states. A named instance or manifest alone does not prove installation fit. Keep hidden closed-shade alternatives out of the normal IFC export; describe them as privacy concepts, not certified blackout systems.
- `render_views.py` writes all named views into ignored `outputs/work/`. Only view 04 hides roof/structure; view 14 lowers shades. Both changes are temporary. Inspect every actual image and secure independent visual review before stable promotion. Final defaults are 1600 × 1100, 64 samples; environment variables `ATRIUM_PERCENT` and `ATRIUM_SAMPLES` support drafts.
- `draw_plan.py` reads measured architecture and the freshly generated actual furniture footprint record. Use `--help` for draft/promotion options. Inspect PNGs and rasterized PDF pages; refresh plan evidence after any layout change.
- `export_ifc.py` uses the shared classified-concept exporter, then reopens and schema-checks IFC4. `verify_bonsai.py` performs a separate fresh import and compares imported envelope mesh bounds. Optional `--runtime-path` is process-local; never change saved user preferences. Export success is not engineering or complete semantic-BIM certification.
- `gallery_cameras.py` is now a read-only fresh camera check against `cameras.py`; rebuild to apply camera changes. It no longer changes a saved scene.
- After reviewed native views, perform the full Imagegen photographic tour. Keep exact source/output hashes and actual prompts in `outputs/photo-prompts.json` and `photo-study.md`. `write_gallery.py` writes full home/output landing pages. The root catalog retains only one photographic hero beside one main plan.

Typical order, from repository root with Blender and the drawing dependencies available:

```sh
blender --background --factory-startup --python-exit-code 1 --python tools/atrium01/build.py
blender --background --factory-startup homes/atrium-01/model/atrium-01.blend --python-exit-code 1 --python tools/atrium01/verify.py
blender --background --factory-startup homes/atrium-01/model/atrium-01.blend --python-exit-code 1 --python tools/atrium01/gallery_cameras.py
blender --background --factory-startup homes/atrium-01/model/atrium-01.blend --python-exit-code 1 --python tools/atrium01/render_views.py
python3 tools/atrium01/draw_plan.py
blender --background --factory-startup homes/atrium-01/model/atrium-01.blend --python-exit-code 1 --python tools/atrium01/export_ifc.py
blender --background --factory-startup --python-exit-code 1 --python tools/atrium01/verify_bonsai.py
python3 tools/atrium01/write_gallery.py
python3 tools/common/verify_galleries.py
```
