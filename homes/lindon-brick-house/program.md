# Lindon Brick House — program and decisions

**Status: first editable remodel concept, with open dimensional and design coordination items.** The native model exists and has reopened successfully. This is not yet a resolved home design, a measured reconstruction or a construction package. See the [design review](design-review.md) for the limits of the recorded checks.

## Brief and source baseline

The user's final direction is **warm textured red brick that feels old-school and modern, with better rectangular windows and clean details**. It supersedes the earlier farmhouse direction. The premium profile guides proposed equipment and finishes; household occupancy and accessibility needs have not been supplied.

Preserve the recognizable angled three-car garage wing, main and upper levels over a walkout basement, two rear decks, pool and court. The source plans are undimensioned: tour 2nd floor = main, 3rd = upper, 1st = basement, as visually mapped. Proposed basement lightwells, stacked rear stairs, rectangular terrace edges and revised roof/window forms are design changes, not claims about the existing house.

| Level | Listing program | Listing area | Measured first-model floor surface |
|---|---|---:|---:|
| Main | Public living/dining, den, kitchen and one half bath; no bedrooms listed | 2,448 sq ft | 2,376.474 sq ft |
| Upper | Five bedrooms, two full baths, one three-quarter bath and laundry | 2,180 sq ft | 2,482.622 sq ft |
| Walkout basement | Two bedrooms, one three-quarter bath, family/recreation, second kitchen and laundry | 2,179 sq ft | 2,409.520 sq ft |
| Occupied floors | Seven bedrooms; five physical bathroom rooms | **6,807 sq ft** | **7,268.616 sq ft** |
| Garage | Three-car attached wing | Not separately established here | 974.124 sq ft |

Model areas are top horizontal mesh faces after stair-void cuts, including walls and excluding terraces, patios and site. Garage is separate; model total including garage is 8,242.740 sq ft. Occupied model area exceeds the listing by **461.616 sq ft, about 6.78%**. This remains an unresolved trace-scale/level-registration issue, not a verified addition or an accepted survey discrepancy. Listing and model area conventions may also differ. Report both rather than forcing the geometry to match an unverified total.

The bathroom schedule remains two full + two three-quarter + one half: **five physical bathrooms**. `project.json` uses a conventional 4.5 shorthand treating a shower bathroom as a full bathroom for display; the itemized schedule controls the actual program. Existing site boundaries, elevations and conditions are unverified; retain the listing's 1.35/1.33-acre discrepancy. See [source references](references/README.md).

## Current modeled choices and open work

The [asset schedule](assets/README.md) and [project manifest](project.json) record **46 pinned dependencies**, including nested materials/hardware. These are adopted links, not a candidate list. [The actual-use audit](model/asset-adoption.json) confirms each pin has direct native placement/material use or a declared adopted parent. This checks reuse, not product suitability or installation performance.

| Area | Current concept and adopted components | Still unresolved |
|---|---|---|
| Exterior | `warm-red-brick/v003` on 156 meshes with named physical-meter brick UVs; dark pitched standing-seam roof, charcoal window fields, warm plaster recesses and smoked-oak entry details | Wall assembly, attachment, flashing, drainage, roof intersections, structure and weather performance; listing solar remains unmodeled |
| Windows and exterior doors | 28 linked `slim-dark-window/v002` assemblies; revised rectangular openings, separate entry/rear door geometry | Window instances are width/height-scaled studies, so frame/profile sizes vary. Publish correct dimensional variants or select products before treating them as specified units. Sash operation, egress, safety glass, thermal performance, privacy and structural opening support are unproven |
| Main and basement kitchens | Both contain shared induction cooktop, oven, wall hood, 48-inch panel-ready refrigerator, dishwasher and sink/mixer. Shared drawer cabinets, fitted worktops, real sink apertures and dedicated oven bays; main pantry modeled | Both cooktop glass surfaces were checked at 5.5 mm above their worktops. Full door/drawer sweeps, remaining mounting interfaces, landing surfaces, actual exhaust discharge, services and replacement routes remain open. Dedicated waste/recycling and complete basement pantry/storage provisions are not demonstrated |
| Bedrooms and clothes storage | One king and six queen linked beds, bedside furniture and wardrobe bays assigned to all seven bedrooms; five bedrooms upper, two basement | Full bed/wardrobe/door operation and access audit, furniture refinements, privacy and local escape strategy. Seven evaluated beds do not prove seven compliant bedrooms |
| Primary suite | Upper suite with linked double basin/vanity arrangement, separate tub and shower, toilet and clothes storage | Dry circulation, WC privacy/door conflicts, fixture service space and wet-area assembly review. Proposed premium fittings are not verified existing equipment |
| Other baths | Linked sanitary fixtures in main powder, upper shared/wing bathrooms and basement bath; source bath distribution retained | Each fixture's standing/cleaning space, door conflicts, ventilation, mounting and product selection |
| Arrival and parking | Angled garage, modeled openings, drive apron, front approach and garage-entry coat wardrobe | Vehicle fit, open doors, turning and continuous pedestrian envelopes. Source foyer coat storage was removed from the proposed stair reservation; front-door drop/coat provision remains incomplete. Eight uncovered listing spaces are not modeled as verified stalls |
| Stairs | Curved foyer flight and two stacked rear flights with treads, risers, landings, guards and coordinated slab voids. Rear lower arrival was moved inside the envelope, facing north; a targeted width-sample/landing check was performed | Headroom throughout the path, winder walking-line dimensions, guard/handrail compliance, structural attachment and replacement storage; source rear stair location was altered |
| Living and recreation | Linked sofas, tables, dining chairs and desk; family-room closed-glass fireplace; basement billiards table | Occupied seating/pullback/cue envelopes, fireplace fuel/air/flue/hearth requirements and acoustics. Fireplace is selected concept geometry, not an existing-equipment claim |
| Laundry and general storage | Shared front-loading modules at upper and basement laundry, linen/storage wardrobes and fitted cabinets | Appliance door/basket space, folding/hanging allocation, supply/drain/vent strategy, cleaning and seasonal storage completeness |
| Lighting and hardware | Linked recessed and linear focal fixtures, actual ceiling cutouts, shared fixture/cabinet pulls | Complete task/mirror/exterior lighting and door-hardware schedules, controls, electrical coordination and mounting/operation checks |
| Rear decks and walkout | Two timber rear terraces, supports/guards, lower patio and garden steps; proposed west basement lightwells | Ground/retaining/drainage engineering, waterproofing, safe guards/barriers and daylight/escape validation. Lightwells are proposed daylight/maintenance features, not certified emergency exits |
| Pool, court and landscape | Shared 6 × 12 m pool, court, chaises, paving and planted assets arranged around the approximate source relationships | These asset sizes are not surveyed property dimensions. Pool barrier/gates/equipment, court safety/runoff, species suitability, property limits and maintenance access remain open; accessory pool structures unmodeled |
| Building services | Listing gas forced-air heat/electric cooling retained as source context; local appliance/hood/chase geometry only | Existing condition, loads, equipment selection, fresh air, zoning, complete plumbing/electrical/HVAC routes and replacement access are not designed |

Additional elevator/lift, sauna, new garage, scullery or separate-dwelling conversion remain outside this first concept. A second kitchen does not establish legal separate occupancy.

## Evidence and output status

[Native verification](model/native-validation.json) records reopening in Blender 4.5.14 LTS, 46 relative dependencies, seven evaluated bed instances, 28 window assemblies, physical brick UV presence and eight cameras. It also records both cooktop mounting heights, upward roof faces and a garage setback cap excluding the upper occupied footprint. [Stair dimensions](model/stair-review.json) and [opening coordinates](model/opening-schedule.json) are concept schedules, not operating/headroom approvals. The IFC schema receipt records zero schema errors; this does not certify a coordinated building model.

The current set contains eight visually inspected native renders and three furnished level plans (PNG + SVG), promoted into the stable output folders and embedded in the home, output and root README galleries. [Output review](model/output-review.json) records the selected files and scope. Presentation review does not close the functional or dimensional items in `design-review.md`.
