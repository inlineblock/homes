# Coastal House

A bright modern coastal home with pale limestone, natural white oak, expansive glazing and a shaded terrace. The kitchen and dining room open directly to outdoor living.

![Coastal House with glass wall open](outputs/images/01-terrace-open.png)

[All current images and plans](outputs/README.md)

The first concept assumes **one story, 2,720 gross enclosed sq ft, three bedrooms and two bathrooms**. The 68 x 40 ft floor plate includes walls; the terrace, eaves and illustrative shore are excluded. These size/program choices can change.

## The two openings

- **Great room:** six sliding panels close a 30 ft wide, approximately 9 ft 5 in tall opening. They slide left into a concealed side pocket, freeing the living/dining threshold.
- **Kitchen pass-through:** four panels close a 12 ft wide opening above the approximately 37-inch counter. They slide right into a separate pocket. Interior and exterior cabinetry support aligned stone counters on both sides, joined beneath the recessed track zone.
- The kitchen island remains separate, with a sink, seating and broad working aisles. The exterior counter has its own drawer faces and stool seating.

![Indoor outdoor serving counter](outputs/images/03-serving-counter-open.png)

## Editable source

Open [coastal-house.blend](model/coastal-house.blend) in Blender 4.5.14 LTS. **Frame 1 = closed; frame 120 = fully open.** Both systems move real modeled panels; the renders do not fake opening by hiding glass. The saved default is open. Four relative library links keep the model portable.

[coastal-house.ifc](model/coastal-house.ifc) contains the closed architectural envelope as classified IFC4 concept geometry, verified by reopening in Bonsai 0.8.5. It excludes most decorative furniture and is not a fully parametric building model.

## Reproduce

Run from the repository root, with Git LFS files materialized:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/coastal04/build.py
/Applications/Blender.app/Contents/MacOS/Blender --background homes/coastal-house/model/coastal-house.blend --python-exit-code 1 --python tools/coastal04/render.py
/Applications/Blender.app/Contents/MacOS/Blender --background homes/coastal-house/model/coastal-house.blend --python-exit-code 1 --python tools/coastal04/verify.py --python tools/common/export_scene_ifc.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/common/verify_bonsai.py -- coastal-house
```

Render drafts go to ignored `outputs/work/`. Review before copying selected views into `outputs/images/`; regenerate the PDF and previews after changing embedded images. Final images are 3200 x 2000, Cycles, 512 maximum samples with adaptive sampling and denoising. To export the closed IFC, run `verify.py` followed by `tools/common/export_scene_ifc.py` in the same Blender process; verification leaves the scene at frame 1 without saving it. Reopen the IFC with `tools/common/verify_bonsai.py -- coastal-house`.

Drawings use the repository's pinned ReportLab/PyPDF dependencies; run `python3 tools/coastal04/draw_plans.py` after promoting images.

Shared assets: original coastal white oak, honed limestone and oak counter stool v001; existing opal pendant v001. The rest of the geometry is original and generated in the Coastal authoring folder.

## Scope

This is a dimensioned architectural concept and editable visualization, not construction documentation. The ocean is an artistic backdrop. No site, flood/wind exposure, structural header, drainage/thermal detail or final sliding product has been approved. [Reference notes](references/README.md) distinguish plausible mechanisms from unresolved engineering.

Original designs/assets: CC BY 4.0, attribution Homes project contributors. Authoring code: MIT.
