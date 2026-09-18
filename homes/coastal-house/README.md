# Coastal House

A bright modern coastal home with pale limestone, natural white oak, expansive glazing and a shaded terrace. The kitchen and dining room open directly to outdoor living.

**Rear terrace — glass wall and serving window open**

![Coastal House with glass wall open](outputs/images/01-terrace-open.png)

[All current images and plans](outputs/README.md)

The current concept assumes **one story, 2,720 gross enclosed sq ft, three bedrooms and two bathrooms**. The 68 x 40 ft floor plate includes walls; the terrace, eaves and illustrative shore are excluded. These size/program choices can change.

## The two openings

- **Great room:** six sliding panels close a 30 ft wide, approximately 9 ft 5 in tall opening. They slide left into a concealed side pocket, freeing the living/dining threshold.
- **Kitchen pass-through:** four panels close a 12 ft wide opening above the approximately 37-inch counter. They slide right into a separate pocket. Interior and exterior cabinetry support aligned stone counters on both sides, joined beneath the recessed track zone.
- The kitchen island remains separate, with a sink, seating and broad working aisles. The exterior counter has its own drawer faces and stool seating.

### Long glass wall — closed comparison

Compare this closed view with the open rear terrace above: the camera stays in the same position, and the modeled panels move along their tracks into side pockets.

![Same rear terrace with glass wall and serving window closed](outputs/images/05-terrace-closed.png)

### Serving counter — open

![Indoor outdoor serving counter](outputs/images/03-serving-counter-open.png)

### Serving counter — closed

The same close camera shows the four glazed panels closing the counter opening. Cabinets remain on both sides; the stone bridge lies beneath the track zone.

![Same indoor outdoor serving counter with sliding panels closed](outputs/images/04-serving-counter-closed.png)

### Living and dining — the inside view

The interior view shows how the long opening connects the dining area to the terrace while the kitchen uses its separate serving window.

![Dining room and kitchen opening toward the coast](outputs/images/02-great-room.png)

## Front arrival, roof and storage

### Front arrival and covered parking

![Front arrival and two-car carport](outputs/images/06-front-arrival.png)

The front now has a **26 x 24 ft two-car carport**, a road-facing drive, a separate 6 ft pedestrian path, and a 4 ft crosswalk behind parked cars. The carport and site work are excluded from the enclosed area. Two original unbranded coupe models illustrate parking envelopes; turning and full door-opening sweeps remain unverified.

The house has a **low 2:12 standing-seam gable roof** above its level ceilings. The carport has a 1:12 slope. Gutters, downpipes and conceptual underground conveyance are modeled. Exact mechanically seamed roofing product, coastal corrosion specification, gutter capacities and a surveyed discharge point require site-specific design.

### Roof and site overview

![Elevated view of the pitched house roof, carport and front approach](outputs/images/07-roof-and-parking.png)

### West garden and side elevation

The side view connects the gable profile, garden and rear outdoor living area.

![West garden, side elevation and rear terrace](outputs/images/08-west-garden.png)

### Daylit entry

![Entry hall with coat storage and a view toward the terrace](outputs/images/09-entry-hall.png)

The entrance is now **8 ft wide and opens after 12 ft**, with a full-height sidelight. A coat wardrobe and shallow drop shelf serve the entry. Laundry linen shelving, a kitchen waste pullout and a 5 x 4.8 ft mechanical/service allowance address everyday needs. Equipment sizing and ventilation remain unengineered. Each guest bedroom has a **6 ft wardrobe, 24 inches deep**, assembled from reusable oak storage bays; the primary wing is enlarged to 18 x 26 ft with an 18 x 12 ft king bedroom, 6 x 6 ft dressing room, separate 6 ft soaking tub, generous shower, enclosed 4 x 6 ft toilet room and double vanity with 36-inch basin centers. Bedroom 02 is a nominal 15 x 12 ft zone and bedroom 03 is 15 x 16 ft. These dimensions include the wardrobe zone and are not net floor areas.

## Complete kitchen and private suite

The kitchen includes a shared **36-inch induction cooktop, 30-inch oven, 36-inch hood, 24-inch dishwasher and 48-inch panel-ready refrigerator**, with actual cabinet bays, sink, waste/recycling pullout and tall pantry. Equipment is original concept geometry; final product clearances, power/water and exterior ventilation remain unengineered.

### Primary vanity and soaking tub

![Primary suite double vanity and soaking tub](outputs/images/10-primary-bath.png)

Shared bronze cabinet pulls and door levers, recessed downlights with real ceiling cutouts and concealed task lighting give the design consistent detail. The primary suite contains a separate shower and tub, enclosed toilet, double vanity and dressing room. A fireplace remains optional and is not included in this coastal concept.

## Single-level floor plan

The furnished plan shows all three bedrooms and their storage, the entry, household service spaces, private suite and both separate glass openings. The bathroom image above shows the vanity and tub; the plan locates the shower, enclosed toilet and dressing room.

![Dimensioned Coastal House single-level floor plan](outputs/plans/floor-plan.png)

[Full-size floor plan](outputs/plans/floor-plan.png) · [Vector floor plan](outputs/plans/floor-plan.svg) · [Arrival and roof site plan](outputs/plans/site-plan.svg) · [Design booklet](outputs/plans/design-board.pdf)

## Editable source

Open [coastal-house.blend](model/coastal-house.blend) in Blender 4.5.14 LTS. **Frame 1 = closed; frame 120 = fully open.** Both systems move real modeled panels; the renders do not fake opening by hiding glass. The saved default is open. Twenty relative library links keep the model portable.

[coastal-house.ifc](model/coastal-house.ifc) contains the closed architectural envelope as classified IFC4 concept geometry, verified by reopening in Bonsai 0.8.5. It excludes most decorative furniture and is not a fully parametric building model.

## Reproduce

Run from the repository root, with Git LFS files materialized:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/coastal04/build.py
/Applications/Blender.app/Contents/MacOS/Blender --background homes/coastal-house/model/coastal-house.blend --python-exit-code 1 --python tools/coastal04/render.py
/Applications/Blender.app/Contents/MacOS/Blender --background homes/coastal-house/model/coastal-house.blend --python-exit-code 1 --python tools/coastal04/verify.py --python tools/common/audit_asset_adoption.py --python tools/common/export_scene_ifc.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/common/verify_bonsai.py -- coastal-house
```

Render drafts go to ignored `outputs/work/`. Review before copying selected views into `outputs/images/`; regenerate the PDF and previews after changing embedded images. Final images are 3200 x 2000, Cycles, 256 maximum samples for front/roof/side and closed-terrace views; 512 for interiors, counter views and the open-terrace hero, all with adaptive sampling and denoising. To export the closed IFC, run `verify.py` followed by `tools/common/export_scene_ifc.py` in the same Blender process; verification leaves the scene at frame 1 without saving it. Reopen the IFC with `tools/common/verify_bonsai.py -- coastal-house`.

Drawings use the repository's pinned ReportLab/PyPDF dependencies; run `python3 tools/coastal04/draw_plans.py` after promoting images.

Shared assets: original coastal white oak, honed limestone and oak counter stool v001; existing opal pendant v001; shared olive tree, 4 ft limestone paver and 2 ft oak wardrobe bays v001; refined sage shrub and ornamental grass v002. Kitchen appliances, bathroom fixtures, layered lighting and bronze hardware are also linked shared assets; see the [complete adoption inventory](assets/README.md). Bespoke house geometry stays in the Coastal authoring folder; generic geometry and furniture helpers live in the common tools.

[Current household program and unresolved checks](program.md)

## Scope

This is a dimensioned architectural concept and editable visualization, not construction documentation. The ocean is an artistic backdrop. No site, flood/wind exposure, structural header, drainage/thermal detail or final sliding product has been approved. [Reference notes](references/README.md) distinguish plausible mechanisms from unresolved engineering.

Original designs/assets: CC BY 4.0, attribution Homes project contributors. Authoring code: MIT.
