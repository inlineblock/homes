# Atrium 01

![Atrium 01 — Imagegen photographic study](outputs/images/photo-hero.png)

*Photorealistic AI study of the design. [Source and prompt](outputs/photo-study.md).*

A kitchen-led, modern Eichler-inspired concept: three bedrooms, three bathrooms, exposed fir beams, walnut cabinetry, pale stone, and a planted central atrium.

### Kitchen: walnut, stone and sage tile

![Kitchen: walnut, stone and sage tile](outputs/images/01-kitchen.png)

### Kitchen toward the courtyard

![Kitchen toward the courtyard](outputs/images/02-kitchen-courtyard.png)

### Front arrival and complete building

![Front arrival and complete building](outputs/images/03-exterior.png)

### Rear glazing and east terrace

![Rear glazing and east terrace](outputs/images/05-rear-terrace.png)

### West side, roof and open atrium

![West side, roof and open atrium](outputs/images/06-west-roof-atrium.png)

### Crowning feature: the open-air atrium

![Crowning feature: the open-air atrium](outputs/images/07-open-air-atrium.png)

### Whole-home cutaway

![Whole-home cutaway](outputs/images/04-cutaway.png)

### Single-level floor plan

![Single-level floor plan](outputs/plans/floor-plan.png)

[Dimensioned PDF](outputs/plans/floor-plan.pdf) · [Vector plan](outputs/plans/floor-plan.svg)

**[Browse all current images and plans](outputs/README.md)** — one current set; previous revisions live in Git.

## Open and review

- `model/atrium-01.blend`: furnished, editable presentation scene, with seven named cameras and a separately switchable roof collection.
- `model/atrium-01.ifc`: IFC4 architectural export for Bonsai, with walls, glazing, structure, slabs, roof, selected kitchen elements, and labeled planning zones.
- `outputs/plans/floor-plan.pdf`: dimensioned concept plan; SVG and PNG versions sit alongside it.
- `outputs/images/`: two complementary kitchen interiors, front arrival, rear terrace, west roof/site, open-air atrium and whole-home cutaway views, rendered directly from the model.

The 60 × 44 ft outer footprint encloses 2,640 sq ft before subtracting the 16 × 15 ft atrium. The resulting **2,400 sq ft is gross enclosed area including wall thickness**, excluding the open courtyard and exterior terraces. There is no garage. Room dimensions on the plan describe planning zones, not finished clear dimensions or an appraised area schedule.

The entry leads through the open-air atrium, an intentional part of this concept. A covered circulation alternative can be developed in a later revision.

## Kitchen

The approximately 10 × 4 ft island seats four and faces the atrium. The south wall combines cooking, original fluted sage tile, and a walnut display shelf. The east run contains the refrigerator, stacked ovens, prep drawers, and an undermount sink. A pantry/laundry room sits beside the entry.

The tile is linked from `../../library/materials/sage-fluted-tile/v001/`. Keep the repository together when moving it. Other furnishings are currently project-local modeled placeholders; they can be promoted into versioned library assets when reused.

## Software and regeneration

Created with Blender **4.5.14 LTS**, Bonsai **0.8.5**, and Cycles using the Mac's Metal GPU. Bonsai is installed as a Blender extension. `project.json` records the model and asset dependencies.

From the repository root, using your Blender executable:

```sh
blender --background --python tools/atrium01/build.py -- --render
blender --background homes/atrium-01/model/atrium-01.blend --python tools/atrium01/export_ifc.py --python tools/atrium01/verify.py --python tools/atrium01/render_views.py
python3 tools/atrium01/draw_plan.py
# Camera-only gallery update, preserving an existing furnished model:
blender --background homes/atrium-01/model/atrium-01.blend --python tools/atrium01/gallery_cameras.py
blender --background homes/atrium-01/model/atrium-01.blend --python tools/atrium01/gallery_cameras.py -- --verify-gallery
```

The drawing tool requires `reportlab`. On this Mac the Blender executable is `/Applications/Blender.app/Contents/MacOS/Blender`; the drawing dependency is available in Codex's bundled Python. Building again overwrites the named model/drawing outputs. The view renderer writes drafts to ignored `outputs/work/`; inspect them before copying to the stable `outputs/images/` filenames. Optional view filenames after `--` select a subset; `ATRIUM_PERCENT` and `ATRIUM_SAMPLES` allow draft settings. The gallery finals use 1,800 × 1,238 pixels and 96 Cycles samples, matching the existing secondary views. Commit or copy any manual edits first. Existing versioned tile library files are reused rather than overwritten.

## Verified scope and limits

The presentation scene reopens with relative library links. The exported IFC passes an IFC4 schema check; validation summaries are saved in `model/`. Rendered views and the PDF plan were visually reviewed.

The IFC was also imported successfully using the installed Bonsai extension, yielding 251 mesh objects. That receipt is in `model/bonsai-validation.json`.

This is an architectural **concept**, not a permit or construction set. Structure, drainage, foundations, insulation assemblies, mechanical systems, electrical/plumbing routes, local code, and site conditions are unresolved. The landscape is illustrative. Appliances and fixtures are schematic, with no manufacturer specification.

The IFC is a classified geometric architectural export, not a fully parametric authoring model: wall segments represent the apertures geometrically, planning spaces are labeled zones without calculated boundaries, and most furniture and detailed materials remain in Blender. It is separate from the presentation scene; edits do not synchronize automatically.


## Gallery review scope

The gallery expansion changes cameras only. Native reopening and a non-camera scene fingerprint confirm that mesh geometry, object transforms, light settings and material assignments stayed unchanged. The new exterior views retain the full roof and structure; only the explicitly labeled cutaway hides them during rendering. The dedicated atrium view shows the original planted courtyard and surrounding glass. See [gallery validation](model/gallery-validation.json) and [review notes](design-review.md).

This older concept has not been redesigned against the newer whole-home program standard. Parking/road access, comprehensive bedroom storage, sheltered atrium circulation and engineered roof drainage remain unresolved; additional photography does not resolve them.
