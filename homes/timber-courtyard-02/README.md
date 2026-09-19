# Timber Courtyard 02

![Timber Courtyard 02 — Imagegen photographic study](outputs/images/photo-hero.png)

*Photorealistic AI study of the design. [Source and prompt](outputs/photo-study.md).*

An exterior-led concept inspired by the user-supplied reference: paired timber-clad wings, dark pitched standing-seam roofs, a transparent central gable, a low entrance canopy, and layered courtyard planting.

![Front arrival and paired timber wings](outputs/images/01-exterior.png)

## Elevated roof and courtyard

![Elevated roof and courtyard](outputs/images/02-elevated.png)

## Courtyard feature

The planted courtyard and glazed entry are the defining feature.

![Garden threshold and courtyard](outputs/images/03-garden-entry.png)

## Rear garden

![Rear elevation and garden](outputs/images/07-rear-garden.png)

## Living room toward the courtyard

A view from the living room through the full-height glazing to the planted courtyard.

![View from the living room through courtyard glazing](outputs/images/05-living-dining.png)

## Kitchen

The existing island, sage backsplash and rear worktop are shown as a schematic interior, not a completed equipment specification.

![Schematic kitchen interior](outputs/images/06-kitchen.png)

## Ground floor

One level; the dimensioned concept plan and roof-off native view show the same courtyard arrangement.

![Ground-floor schematic plan](outputs/plans/floor-plan.png)

[Editable plan SVG](outputs/plans/floor-plan.svg)

![Ground-floor roof-off model view](outputs/images/04-model-plan.png)

**[Browse all current images and plans](outputs/README.md)** — one current set; previous revisions live in Git.

The user clarified that **the reference's exterior is the priority and the interior may change**. This design retains the original three-bedroom, three-bath, approximately 2,400-square-foot brief, with a new internal arrangement rather than copying the image's plan.

## Deliverables

- `model/timber-courtyard-02.blend`: editable furnished scene with seven named cameras, geometry-based cladding and roof seams, and five relative shared-library links.
- `model/timber-courtyard-02.ifc`: classified IFC4 architectural geometry for Bonsai.
- `outputs/plans/design-board.pdf`: exterior render and a schematic dimensioned floor plan on one presentation sheet; PNG preview alongside it.
- `outputs/plans/floor-plan.svg`: editable vector plan, with a PNG preview.
- `outputs/images/`: front arrival, elevated courtyard, garden threshold feature, rear garden, two schematic interiors, and a roof-off model plan.

The 62 × 48 ft floor footprint minus the 24 × 24 ft open courtyard equals **2,400 sq ft gross enclosed**. This includes wall zones and excludes courtyard, overhangs, entry canopy projection, garden, and approach paving. The actual floor slab geometry is checked during validation. No garage is included.

## Shared artifacts

The second home links the first home's sage tile and two assets promoted from Atrium 01: the opal globe pendant and walnut counter stool. New warm cedar and charcoal metal material assets are published for future homes. Every dependency is pinned to `v001` in `project.json`.

The shared procedural geometry and planting helpers are in `tools/common/`. The original reference image stays in an ignored local folder; only the original model and original assets are included in the shareable repository.

## Rebuild

Uses Blender 4.5.14 LTS and Bonsai 0.8.5. From the repository root:

```sh
blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend --python tools/timber02/verify_gallery.py
blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend --python tools/timber02/render_gallery.py -- 05-living-dining 06-kitchen 07-rear-garden
```

The gallery renderer writes candidates to ignored `outputs/work/`; use `--draft` before the view names for quick camera checks. Inspect actual images before replacing the matching files in `outputs/images/`. It never saves a cutaway or render state over the native model. Camera definitions live in `tools/timber02/gallery.py`; `prepare_gallery.py` applies only the three expansion cameras to the existing scene and verifies the non-camera design is unchanged.

For a full design rebuild, run `tools/timber02/build.py`; it recreates all seven named cameras. The common IFC exporter and `tools/timber02/draw_plan.py` remain the architectural export and plan/board entry points. Regenerate the design board if its front image or plan changes.

Install the drawing dependency from `tools/requirements.txt`. The shared fixture files are already in Git LFS; regeneration does not require opening Atrium 01. The library promotion tool records their original source. Save or commit manual changes before regeneration, which overwrites the named deliverables.

## Scope

This is an original **concept model**, not a construction or permit set. Interiors and landscaping are schematic; the exterior's visual proportions and palette received the most attention. Product selections, weatherproofing, roof drainage, wall assemblies, structure, services, code, and site design are unresolved.

The IFC classifies visible geometry; it does not add engineered assemblies, fully parametric wall systems, room boundaries, or an automatic synchronization workflow with Blender. Rendered planting and most furniture stay in the native presentation scene.

## Known model limitations

This camera-only gallery extension preserves the older concept geometry. The dining chairs lack modeled legs, the coffee table lacks a base, and the kitchen has no modeled oven or extraction hood; cabinetry, appliance details and planting remain schematic. The courtyard-facing living view does not depict the unresolved dining furniture. These are recorded gaps, not a completed interior design or full visual-quality approval.
