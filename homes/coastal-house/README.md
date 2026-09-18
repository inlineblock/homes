# Coastal House

A bright modern coastal home with pale limestone, natural white oak, expansive glazing and a shaded terrace. The kitchen and dining room open directly to outdoor living.

![Coastal House with glass wall open](outputs/images/01-terrace-open.png)

[All current images and plans](outputs/README.md)

The current concept assumes **one story, 2,720 gross enclosed sq ft, three bedrooms and two bathrooms**. The 68 x 40 ft floor plate includes walls; the terrace, eaves and illustrative shore are excluded. These size/program choices can change.

## The two openings

- **Great room:** six sliding panels close a 30 ft wide, approximately 9 ft 5 in tall opening. They slide left into a concealed side pocket, freeing the living/dining threshold.
- **Kitchen pass-through:** four panels close a 12 ft wide opening above the approximately 37-inch counter. They slide right into a separate pocket. Interior and exterior cabinetry support aligned stone counters on both sides, joined beneath the recessed track zone.
- The kitchen island remains separate, with a sink, seating and broad working aisles. The exterior counter has its own drawer faces and stool seating.

![Indoor outdoor serving counter](outputs/images/03-serving-counter-open.png)

## Front arrival, roof and storage

![Front arrival and two-car carport](outputs/images/06-front-arrival.png)

The front now has a **26 x 24 ft two-car carport**, a road-facing drive, a separate 6 ft pedestrian path, and a 4 ft crosswalk behind parked cars. The carport and site work are excluded from the enclosed area. Two original unbranded coupe models illustrate parking envelopes; turning and full door-opening sweeps remain unverified.

The house has a **low 2:12 standing-seam gable roof** above its level ceilings. The carport has a 1:12 slope. Gutters, downpipes and conceptual underground conveyance are modeled. Exact mechanically seamed roofing product, coastal corrosion specification, gutter capacities and a surveyed discharge point require site-specific design.

The entrance is now **8 ft wide and opens after 12 ft**, with a full-height sidelight. A coat wardrobe and shallow drop shelf serve the entry. Laundry linen shelving, a kitchen waste pullout and a 5 x 4.8 ft mechanical/service allowance address everyday needs. Equipment sizing and ventilation remain unengineered. Each guest bedroom has a **6 ft wardrobe, 24 inches deep**, assembled from reusable oak storage bays; the primary wing is enlarged to 18 x 26 ft with an 18 x 12 ft king bedroom, 6 x 6 ft dressing room, separate 6 ft soaking tub, generous shower, enclosed 4 x 6 ft toilet room and double vanity with 36-inch basin centers. Bedroom 02 is a nominal 15 x 12 ft zone and bedroom 03 is 15 x 16 ft. These dimensions include the wardrobe zone and are not net floor areas.

## Complete kitchen and private suite

The kitchen includes a shared **36-inch induction cooktop, 30-inch oven, 36-inch hood, 24-inch dishwasher and 48-inch panel-ready refrigerator**, with actual cabinet bays, sink, waste/recycling pullout and tall pantry. Equipment is original concept geometry; final product clearances, power/water and exterior ventilation remain unengineered.

![Primary suite bathroom](outputs/images/10-primary-bath.png)

Shared bronze cabinet pulls and door levers, recessed downlights with real ceiling cutouts and concealed task lighting give the design consistent detail. The primary suite contains a separate shower and tub, enclosed toilet, double vanity and dressing room. A fireplace remains optional and is not included in this coastal concept.

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
