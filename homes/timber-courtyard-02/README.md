# Timber Courtyard 02

An exterior-led concept inspired by the user-supplied reference: paired timber-clad wings, dark pitched standing-seam roofs, a transparent central gable, a low entrance canopy, and layered courtyard planting.

![Exterior](renders/01-exterior.png)

The user clarified that **the reference's exterior is the priority and the interior may change**. This design retains the original three-bedroom, three-bath, approximately 2,400-square-foot brief, with a new internal arrangement rather than copying the image's plan.

## Deliverables

- `model/timber-courtyard-02.blend`: editable furnished scene with four named cameras, geometry-based cladding and roof seams, and five relative shared-library links.
- `model/timber-courtyard-02.ifc`: classified IFC4 architectural geometry for Bonsai.
- `drawings/design-board.pdf`: exterior render and a schematic dimensioned floor plan on one presentation sheet; PNG preview alongside it.
- `drawings/floor-plan.svg`: editable vector plan, with a PNG preview.
- `renders/`: front exterior, elevated courtyard view, garden entry, and roof-off model plan.

The 62 × 48 ft floor footprint minus the 24 × 24 ft open courtyard equals **2,400 sq ft gross enclosed**. This includes wall zones and excludes courtyard, overhangs, entry canopy projection, garden, and approach paving. The actual floor slab geometry is checked during validation. No garage is included.

## Shared artifacts

The second home links the first home's sage tile and two assets promoted from Atrium 01: the opal globe pendant and walnut counter stool. New warm cedar and charcoal metal material assets are published for future homes. Every dependency is pinned to `v001` in `project.json`.

The shared procedural geometry and planting helpers are in `tools/common/`. The original reference image stays in an ignored local folder; only the original model and original assets are included in the shareable repository.

## Rebuild

Uses Blender 4.5.14 LTS and Bonsai 0.8.5. From the repository root:

```sh
blender --background --python tools/timber02/build.py -- --render
blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend --python tools/common/export_scene_ifc.py --python tools/timber02/verify_render.py
python3 tools/timber02/draw_plan.py
```

Install the drawing dependency from `tools/requirements.txt`. The shared fixture files are already in Git LFS; regeneration does not require opening Atrium 01. The library promotion tool records their original source. Save or commit manual changes before regeneration, which overwrites the named deliverables.

## Scope

This is an original **concept model**, not a construction or permit set. Interiors and landscaping are schematic; the exterior's visual proportions and palette received the most attention. Product selections, weatherproofing, roof drainage, wall assemblies, structure, services, code, and site design are unresolved.

The IFC classifies visible geometry; it does not add engineered assemblies, fully parametric wall systems, room boundaries, or an automatic synchronization workflow with Blender. Rendered planting and most furniture stay in the native presentation scene.
