# Timber Courtyard 02

![Paired timber wings and courtyard arrival — AI photographic study](outputs/images/photo-hero.png)

*AI photographic study. [Sources, prompts and visual review](outputs/photo-study.md).*

An exterior-led, single-level courtyard home with a newly coordinated kitchen, fitted pantry and living room. **2,400 sq ft gross enclosed · 3 bedrooms · 3 baths.** The kitchen revision addresses the missing cooking equipment and storage exposed by the walkthrough; the rest of the legacy home program remains unresolved.

## Walkthrough

[Walkthrough, photographic reference frames and current video status](outputs/videos/README.md)

The route travels from the front approach through the courtyard into the living room and revised kitchen. **[Watch the reviewed AI-finished walkthrough](outputs/videos/timber-courtyard-ai.mp4)**: 26 seconds of moving-camera footage with one deliberate cut from the living-room pause to the kitchen approach. The **[continuous 30-second Blender version](outputs/videos/timber-courtyard-native.mp4)** preserves the full route. Both passed decoding and browser playback checks; the video index records visual review, fifteen photographic reference checkpoints and the exact edit. The AI film is an architectural concept visualization, not footage of a built house.

## Arrival and courtyard

Paired cedar wings, dark pitched roofs and a glazed central gable frame the planted courtyard. The low entrance canopy and stepping-stone approach preserve the exterior-led design.

![Front timber wings, glazed gable and courtyard approach](outputs/images/01-exterior.png)

![Elevated pitched roofs and courtyard relationship](outputs/images/02-elevated.png)

![Planted courtyard and garden entry](outputs/images/03-garden-entry.png)

## Kitchen

A complete modeled cooking and cleanup arrangement replaces the old placeholders: a 36-inch induction cooktop, 30-inch oven, 36-inch hood, 48-inch panel-ready refrigerator/freezer, sink and integrated dishwasher. The 7 ft 9 in × 4 ft island seats three; deep drawers, waste storage and working clearances are part of the native model.

![Kitchen, preparation island and garden-facing cleanup counter — AI photographic study](outputs/images/photo-kitchen.png)

![Native kitchen source — island, cleanup counter and storage](outputs/images/06-kitchen.png)

## Cooking wall

Smoked-oak cabinetry, pale honed stone, restrained sage tile and bronze details sit under a finished timber ceiling. The oven housing, cooktop opening, extractor and appliance fronts are modeled shared assets; final commercial product selection and services remain to be coordinated.

![Induction cooking wall, built-in oven and integrated refrigeration — AI photographic study](outputs/images/photo-cooking-wall.png)

![Native cooking-wall source — cooktop, oven, hood and wide integrated refrigeration](outputs/images/08-cooking-wall.png)

## Walk-in pantry

The existing 8 × 16 ft pantry is fitted with shallow food shelves, deeper storage drawers, a worktop, lighting and power outlets. Its side glazing is raised above the seven-foot shelving, with solid backing behind the storage.

![Fitted pantry shelving and appliance worktop — AI photographic study](outputs/images/photo-pantry.png)

![Native pantry source — fitted shelves and rear worktop](outputs/images/09-pantry.png)

## Living room

A linen sofa, rounded oak coffee table and dining furniture are linked from the shared library. The sloping cedar lining ties these rooms to the kitchen and courtyard.

![Living room, shared furnishings and timber ceiling — AI photographic study](outputs/images/photo-living-room.png)

![Native living-room source — supported furnishings and timber ceiling](outputs/images/10-living-room.png)

![Living room looking through the glazing into the courtyard](outputs/images/05-living-dining.png)

## Rear garden

Kitchen glazing now starts above the worktop with a solid cedar-clad wall below. Full-height living-room glazing remains alongside it. The wider site and landscape are conceptual.

![Rear garden and revised kitchen glazing — AI photographic study](outputs/images/photo-rear-garden.png)

![Rear garden elevation with counter-height kitchen glazing](outputs/images/07-rear-garden.png)

## Ground floor

The dimensioned concept plan and roof-off native view show the same single-level courtyard arrangement.

![Furnished concept floor plan with revised kitchen and pantry](outputs/plans/floor-plan.png)

[Editable plan SVG](outputs/plans/floor-plan.svg) · [Concept presentation PDF](outputs/plans/design-board.pdf)

![Roof-off model view with revised kitchen, pantry and living furnishings](outputs/images/04-model-plan.png)

## Shared assets and design evidence

The kitchen uses versioned shared cabinet modules, integrated appliances, cooking equipment, sink and mixer, power outlets, lighting and furniture. Exact adopted IDs and versions are pinned in [project.json](project.json) and described in the [asset-use schedule](assets/README.md). The [cooking-appliance catalog](../../library/appliances/README.md) also offers freestanding ranges, gas and induction cooktops, double ovens and oven/speed-oven combinations; those alternatives are not all installed in this home.

Read the [design intent](design-intent.md), [kitchen program](program.md) and [design review](design-review.md) for decisions, measured checks and unresolved work. Exact-fit worktops, room enclosure, ceiling lining and the conceptual exhaust route remain home-specific geometry.

## Deliverables and area

- [Blender model](model/timber-courtyard-02.blend): editable furnished scene with ten named gallery cameras and relative, version-pinned library dependencies.
- [IFC model](model/timber-courtyard-02.ifc): classified concept architectural geometry for Bonsai; furniture and most planting remain in the presentation scene.
- [Current output index](outputs/README.md): reviewed native renders, AI photographic studies, plan, presentation sheet and video index.
- [Photo provenance](outputs/photo-study.md): actual Imagegen prompts, native-source hashes, selected-image hashes and visual-review notes.

The 62 × 48 ft outer footprint less the 24 × 24 ft open courtyard equals **2,400 sq ft gross enclosed**, including wall zones. Courtyard, overhangs, canopy projection, garden and approach paving are excluded. No garage is included. The supplied reference informed the exterior; its interior diagram was not a requirement, and the reference image is excluded from the shareable repository.

## Rebuild

Authoring uses Blender 4.5.14 LTS and Bonsai 0.8.5. From the repository root:

```sh
blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend --python tools/timber02/verify_gallery.py
blender --background homes/timber-courtyard-02/model/timber-courtyard-02.blend --python tools/timber02/render_gallery.py -- 01-exterior 02-elevated 03-garden-entry 04-model-plan 05-living-dining 06-kitchen 07-rear-garden 08-cooking-wall 09-pantry 10-living-room
```

The gallery renderer writes candidates to ignored `outputs/work/`; add `--draft` before the view names for quick checks. Inspect images before promoting them to their stable paths. Camera definitions live in `tools/timber02/gallery.py`. A full `tools/timber02/build.py` rebuild installs the coordinated kitchen and all ten cameras. For the kitchen-only revision workflow, see `tools/timber02/revise_kitchen.py` and `tools/timber02/verify_kitchen.py`; the latter accepts `--file` to check a saved model.

The common IFC exporter and `tools/timber02/draw_plan.py` generate the concept export and plan/board. Install drawing dependencies from `tools/requirements.txt`. Regenerate the board when its exterior image or plan changes. Save manual work before rebuilding. Shared native assets are included through Git LFS; downloads and render caches stay outside the committed deliverables.

## Scope and remaining work

This is an original **architectural concept**, not construction or permit documentation. The kitchen has modeled equipment, storage and reviewed geometry, but appliance product selection, ventilation sizing, utility connections and installation requirements remain unresolved. Measured fit does not establish manufacturer or code approval.

The legacy whole-home program still needs complete bedroom storage, premium bathroom fitout, laundry/services and a real road, parking and site arrangement. Climate, roof drainage, weatherproofing, assemblies, structure and site conditions are unverified. The IFC does not provide engineered assemblies, complete semantic systems, room boundaries or automatic synchronization with Blender. The photographic studies interpret material and landscape detail; the native model and concept plan remain the design sources.
