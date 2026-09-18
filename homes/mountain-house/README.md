# Mountain House

A wood-clad hillside home with two levels total: road-level living and an integrated two-car garage above a downhill walkout level. A 14-foot-deep rear deck wraps around one side, with a partial timber pergola and a shaded patio below.

The timber finish uses neutral brown cedar and deeper thermo-ash, with physical-scale grain following each board and beam, individual grain/tone variation and a matte surface. These shared material revisions replace the earlier pale peach appearance without changing the house geometry or lighting.

![Mountain House forest elevation](outputs/images/01-forest-rear.png)

[Current images and plans](outputs/README.md) · [Concept booklet](outputs/plans/design-board.pdf) · [Editable Blender model](model/mountain-house.blend) · [Classified IFC concept](model/mountain-house.ifc)

## Brief and program

The user requested two levels total, a built-in garage at the front road, a wooded downhill site, predominantly wood exterior, a walkout basement and a large deck to compensate for limited usable yard. The concept assumes three bedrooms and 2.5 baths; no actual parcel, survey or jurisdiction was supplied.

Main floor: open living/dining/kitchen facing the trees, primary suite with walk-in clothes storage, double vanity, separate shower/tub and enclosed toilet room, powder room, mudroom/coat storage, U stair and 24 x 24 ft integrated garage. Lower level: two bedrooms with dedicated wardrobes, shared bath, lounge opening to the patio, laundry/linen and mechanical/workshop allowance. Bedrooms are placed along the exposed rear, not the buried front.

## Area and dimensions

- Exterior main footprint: 60 x 40 ft. Main enclosed floor: 2,280 sq ft after excluding the 120 sq ft stair opening.
- Lower L-shaped footprint: 1,824 sq ft. No occupied lower room beneath the front garage.
- Total gross enclosed floor: 4,104 sq ft including walls and the 576 sq ft garage. Conditioned gross: 3,528 sq ft; this is not measured net living area.
- Rear deck: 60 x 14 ft; side return: 8 x 36 ft. Total deck: 1,128 sq ft, excluded from enclosed area.
- Main datum 0 ft; lower datum -11 ft. Lower patio -11.14 ft with a local grading bench; surrounding slope continues downhill.

The kitchen includes shared cooktop, oven, hood, dishwasher and 48-inch panel-ready refrigeration. A fireplace is selected for Mountain. [Program and explicit choices](program.md) records modeled provisions and unresolved product/engineering decisions.

## Files and reproducibility

Blender 4.5.14 LTS / Bonsai 0.8.5. Meters internally; feet/inches in drawings. Authoring modules are in `tools/mountain05/`; pinned assets are listed in `project.json` and [asset-use schedule](assets/README.md). Review scope is recorded in [design review](design-review.md).

From the repository root, run Blender with `--background --python-exit-code 1 --python tools/mountain05/build.py`. This replaces the generated native model; preserve manual edits first. Open the saved model and run `tools/mountain05/render.py` to create review drafts, with optional view slugs after `--`. Images are 3200 x 2000 with Cycles adaptive sampling and denoising; the final view receipt records 256 or 512 maximum samples by view. Inspect drafts before copying current selected images into `outputs/images/`. Run `tools/mountain05/draw_plans.py` with the documented PDF dependencies. Run the common IFC exporter from the saved scene and Bonsai verifier with `-- mountain-house`.

This is an editable architectural visualization and dimensioned concept, not construction documentation. A real project needs a survey, geotechnical/retaining design, structural and snow-load engineering, local egress/fire review, roof system/drainage design, energy and mechanical design, and site-specific approvals. Terrain, trees and road are original illustrations.
