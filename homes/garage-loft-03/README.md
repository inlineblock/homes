# Garage Loft 03

A modern two-bay garage with four-car pit parking and a heated/cooled game room above. Warm cedar, pale plaster, and dark metal tie it to the shared home collection.

![Garage and game-room exterior](outputs/images/01-exterior.png)

**[Browse current images and plans](outputs/README.md)** · [Concept book](outputs/plans/garage-loft.pdf)

## Parking below, game room above

- A **36 x 28 ft** building footprint, with a separate front door and enclosed return stair to the upper room.
- A **KLAUS MultiBase 2072i-style double-platform pit system** for four passenger/sports cars. Two cars sit at driveway level while the other pair is below grade. The common carriage raises to bring the lower pair to the driveway; the upper pair remains aboard. Either level is accessible without first removing the other cars. The equipment must be unoccupied during movement.
- A pit allowance of **22 x 19 ft**, approximately **six feet deep**, with a modeled front-to-rear drainage fall. Actual pit detailing remains open.
- **12 ft clear garage height**, with the upper finished floor at **13 ft 6 in**. Clearance is needed above grade when the lower cars are retrieved; the pit does not eliminate that requirement.
- An **eight-foot pool table**, a 13 ft 4 in x 17 ft cue envelope, lounge, media wall, refreshments counter, and gaming desk. The upper room has a 9 ft concept ceiling.
- A dedicated upstairs air-source heat pump provides the heating/cooling concept. The model includes an indoor head and outdoor unit; capacity, performance in local climate, insulation, fresh air, and condensate routing have not been designed. Garage ventilation is separate and unresolved.

The car and parking equipment meshes are **original schematic proxies**, not KLAUS CAD or a manufacturer-approved configuration. The supplier's current dimensions and the concept assumptions are recorded in [planning sources](references/README.md).

## Files and area convention

- `model/garage-loft-03.blend`: editable visualization with named cameras, linked assets, a real pit and stair opening, and the lift's stored state as the default.
- `model/garage-loft-03.ifc`: classified architectural geometry with pit, ground-floor, and game-room storeys. It is separate from Blender, with no automatic synchronization. Detailed cars, lift components and furniture remain in the Blender scene.
- `outputs/images/`: exterior, game room, stored garage, building cutaway, and raised retrieval views.
- `outputs/plans/garage-loft.pdf`: three-page concept book covering the exterior, both floors, and both lift states. Editable SVG plans and section sit beside it.

The ground footprint is **1,008 sq ft**, including the parking-pit projection. The upper slab is **895.5 sq ft**, excluding the **112.5 sq ft stair opening**. Combined projected floor area is **1,903.5 sq ft**, including wall zones and garage parking surfaces. This is not living area or an appraised measurement. It excludes roof overhangs, outdoor equipment pad, and paving. The main upstairs room inside the wall lines is approximately 27 x 27 ft; the remaining upper area serves stair arrival and the rear desk zone. No bathroom or plumbing fixtures are currently included.

## Reuse and regenerate

Reuses cedar, charcoal metal, opal pendants, and walnut stools. Adds original reusable `fixtures/double-pit-parking-carriage/v001` and `furniture/walnut-eight-foot-pool-table/v001`. Dependencies are pinned in `project.json`; retain the complete repository for relative links.

Created with Blender 4.5.14 LTS and Bonsai 0.8.5. From the repo root:

```sh
blender --background --python-exit-code 1 --python tools/garage03/build.py --python tools/garage03/render.py
blender --background homes/garage-loft-03/model/garage-loft-03.blend --python-exit-code 1 --python tools/garage03/verify.py --python tools/common/export_scene_ifc.py
python3 tools/garage03/draw_plans.py
blender --background --python-exit-code 1 --python tools/common/verify_bonsai.py -- garage-loft-03
```

Install drawing dependencies with `pip install -r tools/requirements.txt`. Draft views and PDF intermediates go to ignored `outputs/work/`. Inspect their actual pixels and rendered PDF pages, then replace the stable files in `outputs/images/` and `outputs/plans/`; update the galleries. Commit manual model changes before regeneration, which overwrites the native model. Shared versioned assets are reused rather than overwritten.

## Verified scope

The native model reopens with all six relative library links. Geometric checks confirm four car proxies, 1,903.5 sq ft projected floor area, the actual stair opening, the clear cue envelope, and a 10.3 ft raised car top below the 12 ft garage ceiling. The IFC has three storeys, zero schema errors, and imports through Bonsai as 529 mesh objects. Receipts are in `model/`. All five rendered views and all three concept-book pages were visually reviewed. These are concept checks, not equipment or building approval.

## Concept limits

A site has not been assigned. Pit excavation, soil/groundwater, retaining structure, drainage and waterproofing, lift anchorage and safeguards, overhead door travel, floor spans and pool-table point loads, stair/egress, fire and acoustic separation, accessibility, garage ventilation, and HVAC sizing require project-specific professional and manufacturer design. Slab thicknesses and structural members shown are spatial allowances only. The room is a game room, not a dwelling or bedroom. No construction or code approval is implied.
