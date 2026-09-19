# Garage Loft 03

![Garage Loft 03 — Imagegen photographic study](outputs/images/photo-hero.png)

*Photorealistic AI study of the design. [Source and prompt](outputs/photo-study.md).*

A modern two-bay garage with four-car pit parking and a heated/cooled game room above. Warm cedar, pale plaster, and dark metal tie it to the shared home collection.

![Garage and game-room exterior](outputs/images/01-exterior.png)

**[Browse current images and plans](outputs/README.md)** · [Concept book](outputs/plans/garage-loft.pdf)

## Around the complete building

The arrival view above shows the separate pedestrian entrance and two-car-width garage opening. These complementary views keep the full building envelope visible; they do not hide walls or the roof.

| Rear garden and west elevation | Elevated west-side approach |
| --- | --- |
| [![Rear garden and complete garage envelope](outputs/images/07-rear-garden.png)](outputs/images/07-rear-garden.png) | [![Roof, west glazing and front arrival together](outputs/images/08-elevated-approach.png)](outputs/images/08-elevated-approach.png) |
| Rear wall, roof edge and the side of the upstairs room | Roof form, upstairs glazing, garage forecourt and pedestrian entry |

## Upstairs game room

[![Eight-foot pool table and upstairs lounge](outputs/images/02-game-room.png)](outputs/images/02-game-room.png)

The eight-foot pool table is the focus upstairs, with a separate lounge, refreshments counter and dedicated heat-pump head. This is a room-level interior view from the furnished native model.

## Four cars in two bays

| Garage interior, lift stored | Dedicated lift-feature view, lower pair retrieved |
| --- | --- |
| [![Garage interior with two cars at driveway level](outputs/images/03-garage-stored.png)](outputs/images/03-garage-stored.png) | [![Raised carriage revealing both pairs of cars](outputs/images/05-raised-retrieval.png)](outputs/images/05-raised-retrieval.png) |
| Two cars remain below the visible pair; the fixed apron stays separate | The lower pair reaches driveway level while the upper pair stays aboard |

The garage door is omitted in these equipment views. This is an original schematic lift concept; the platform must be unoccupied during movement, and the supplier must resolve safeguards, actual vehicle fit and installation.

[![Technical cutaway showing the parking pit and game room above](outputs/images/04-pit-section.png)](outputs/images/04-pit-section.png)

This dedicated building-and-pit cutaway exposes both parking levels and the upstairs pool table. It is a technical view, separate from the three complete exterior views above.

## Parking below, game room above

- A **36 x 34 ft** building footprint, with an internal garage-to-stair door, separate front door, and enclosed return stair to the upper room.
- A **KLAUS MultiBase 2072i-style double-platform pit system** for four passenger/sports cars. Two cars sit at driveway level while the other pair is below grade. The common carriage raises to bring the lower pair to the driveway; the upper pair remains aboard. Either level is accessible without first removing the other cars. The equipment must be unoccupied during movement.
- A pit allowance of **22 x 19 ft**, approximately **six feet deep**, with a modeled front-to-rear drainage fall. Actual pit detailing remains open.
- **12 ft clear garage height**, with the upper finished floor at **13 ft 6 in**. Clearance is needed above grade when the lower cars are retrieved; the pit does not eliminate that requirement.
- An **eight-foot pool table**, a 13 ft 4 in x 17 ft cue envelope, lounge, media wall, refreshments counter, and gaming desk. The upper room has a 9 ft concept ceiling.
- A dedicated upstairs air-source heat pump provides the heating/cooling concept. The model includes an indoor head and outdoor unit; capacity, performance in local climate, insulation, fresh air, and condensate routing have not been designed. Garage ventilation is separate and unresolved.

The cars are original detailed envelope illustrations, and the parking equipment meshes are **original schematic proxies**, not KLAUS CAD or a manufacturer-approved configuration. The supplier's current dimensions and the concept assumptions are recorded in [planning sources](references/README.md).

## Presentation quality

The editable scene includes curved coupe bodywork and glazing, real wheel-arch cuts, detailed alloy wheels and lights, finer cedar/walnut finishes, upholstery and cabinetry detail, architectural lighting, and a designed forecourt. The cars are unbranded illustrations, not dimensional substitutes for actual vehicles. Native geometry remains the basis of every image.

Final presentation renders use Blender Cycles at 2,560 x 1,850 pixels and 192 samples with denoising. Smaller previews are for iteration only. More image resolution is not a substitute for reviewed geometry, circulation, material scale, or composition.

## Files and area convention

- `model/garage-loft-03.blend`: editable visualization with named cameras, linked assets, a real pit and stair opening, and the lift's stored state as the default.
- `model/garage-loft-03.ifc`: classified architectural geometry with pit, ground-floor, and game-room storeys. It is separate from Blender, with no automatic synchronization. Detailed cars, lift components and furniture remain in the Blender scene.
- `outputs/images/`: three complete exterior angles, game-room and garage interiors, plus building/pit, raised-lift and circulation feature views.
- `outputs/plans/garage-loft.pdf`: four-page concept book covering the exterior, both floors, and both lift states and a dedicated human-access page. Editable SVG plans and section sit beside it.

The ground footprint is **1,224 sq ft**, including the parking-pit projection. The upper slab is **1,111.5 sq ft**, excluding the **112.5 sq ft stair opening**. Combined projected floor area is **2,335.5 sq ft**, including wall zones and garage parking surfaces. This is not living area or an appraised measurement. It excludes roof overhangs, outdoor equipment pad, and paving. The main upstairs room inside the wall lines is approximately 27 x 33 ft; the remaining upper area serves stair arrival and the rear desk zone. No bathroom or plumbing fixtures are currently included.

## Plans for both occupied levels

| Ground floor — garage, operator bay and stair lobby | Upper floor — pool table, lounge and stair arrival |
| --- | --- |
| [![Ground-floor garage and fixed pedestrian route](outputs/plans/ground-plan.png)](outputs/plans/ground-plan.svg) | [![Upper game-room floor plan and pool cue space](outputs/plans/upper-plan.png)](outputs/plans/upper-plan.svg) |

The below-grade pit is unoccupied equipment space. Its dimensions and both platform positions are shown in the [lift section](outputs/plans/lift-section.svg) and [concept book](outputs/plans/garage-loft.pdf).

## Reuse and regenerate

Reuses cedar, charcoal metal, opal pendants, and walnut stools. Uses original reusable `fixtures/double-pit-parking-carriage/v002`, refined `furniture/walnut-eight-foot-pool-table/v002`, and `materials/warm-vertical-cedar/v002`. Earlier published asset versions remain available to the other homes. Dependencies are pinned in `project.json`; retain the complete repository for relative links.

Created with Blender 4.5.14 LTS and Bonsai 0.8.5. From the repo root:

```sh
blender --background --python-exit-code 1 --python tools/garage03/build.py --python tools/garage03/render.py
blender --background homes/garage-loft-03/model/garage-loft-03.blend --python-exit-code 1 --python tools/garage03/verify.py --python tools/common/export_scene_ifc.py
python3 tools/garage03/draw_plans.py
blender --background --python-exit-code 1 --python tools/common/verify_bonsai.py -- garage-loft-03
```

To add the gallery cameras to an existing approved model without rebuilding its geometry, open that model and run `tools/garage03/update_gallery_cameras.py`. The camera positions are shared with the full generator in `tools/garage03/cameras.py`. To regenerate only the two additional views:

```sh
blender --background homes/garage-loft-03/model/garage-loft-03.blend --python-exit-code 1 --python tools/garage03/render.py -- 07-rear-garden 08-elevated-approach
```

Install drawing dependencies with `pip install -r tools/requirements.txt`. Draft views and PDF intermediates go to ignored `outputs/work/`. Inspect their actual pixels and rendered PDF pages, then replace the stable files in `outputs/images/` and `outputs/plans/`; update the galleries. Commit manual model changes before regeneration, which overwrites the native model. Shared versioned assets are reused rather than overwritten.

## Human access and operation

The previous 36 x 28 ft layout had a solid stair separation wall, no internal stair access, an inadequate front apron, and no defined operator position. Those were design omissions. This layout adds six feet of building depth and reorganizes access:

- **7 ft 6 in fixed-floor apron** ahead of the pit, including a **3 ft 6 in pedestrian cross aisle**. Its route to the stair stays outside the lift/pit envelope with either parking level selected. Pause pedestrian crossing while vehicles drive across it.
- **3 x 3 ft operator bay** at the front-right corner on permanent slab, separate from the cross aisle. The control pedestal faces the bay; the person faces the lift. Actual vehicle occlusion and the supplier's required control position remain to be checked.
- **42-inch internal doorway allowance**, opening into a **6 ft 6 in deep stair lobby**. The leaf is hinged at the front jamb and swings into the lobby, clear of the first riser and walking route. Door frame clear width, closing hardware, and fire rating remain design tasks. The separate exterior entrance is shifted east to clear that open leaf.
- The **platform entrance aligns with the fixed apron**. Drivers walk along the stationary selected deck toward its front, then onto fixed floor. The shifted car positions prioritize left-side driver exit; passengers unload before parking. These proxies do not verify real car-door opening arcs, accessibility, or every sports car.
- Side/rear enclosure and a **front access-enclosure reservation** make the separation visible. Front panels are shown closed in stored/raised renders and omitted in the circulation view to show access when stopped and aligned. Their opening mechanism, interlocks, reach protection, and sightlines require KLAUS coordination. The schematic enclosure and floor paint are not certified safeguards.

![Fixed apron, operator and internal stair access](outputs/images/06-circulation.png)

## Verified scope

The revised native model reopens with all six relative library links. Saved-geometry checks confirm a continuous 36-inch pedestrian envelope from the apron through the open internal doorway to the stair lobby with both lift positions, plus a separate entrance-to-stair route. The modeled door leaf does not block those paths; the linked platform front aligns with the fixed slab. These checks do **not** validate car-door articulation or lift safety.

Other checks cover four car proxies, 2,335.5 sq ft projected floor area, the actual stair opening, the pool cue envelope, and a roughly 9.8 ft raised car top below the 12 ft concept ceiling. The IFC has three storeys and zero schema errors. Receipts are in `model/`. Render and drawing review is a concept quality check, not equipment or building approval.

The gallery expansion changes cameras only. A before/after content fingerprint and fresh reopen check preserve the existing geometry, material inputs, lights and stored lift state; the existing IFC and floor drawings remain applicable. See `model/gallery-camera-validation.json` and the current `model/render-validation.json` for the camera and image review evidence.

## Concept limits

A site has not been assigned. Pit excavation, soil/groundwater, retaining structure, drainage and waterproofing, lift anchorage and safeguards, overhead door travel, floor spans and pool-table point loads, stair/egress, fire and acoustic separation, accessibility, garage ventilation, and HVAC sizing require project-specific professional and manufacturer design. Slab thicknesses and structural members shown are spatial allowances only. The room is a game room, not a dwelling or bedroom. No construction or code approval is implied.
