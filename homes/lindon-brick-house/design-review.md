# Lindon Brick House — revised exterior review

**Disposition: editable exterior revision; not a resolved design.** Recorded checks establish a reusable native model and selected geometric facts. Dimensional reconciliation and full functional coordination remain open. The user requested red brick with old-school character and modern styling, then rejected the first all-brick palette. The current revision follows the latest brick-base, charcoal-bay and subdued-taupe direction; appearance review is not client approval.

## Exterior composition and color revision

The user rejected the prior cream finish as too white and its full-height connectors as vertical stripes. The current source replaces it with shared `mushroom-mineral-plaster/v001`, a lower-albedo, low-chroma warm gray-brown finish. Existing deep iron-red brick v003, charcoal panel v001, charcoal roof v002, bronze window v002 and smoked-oak entry assets remain adopted; the earlier plaster stays available to other projects.

Brick now forms the lower level, including the entry and garage connectors. The complete stacked-window bay immediately right of the entry is charcoal through its gable: both storeys, cheeks, side returns, window reveals and exposed slab edges follow the same field. Upstairs, the main recessed volumes and outer garage end wrap in mushroom; the front bay, upper garage window walls and rear bathing volume are charcoal. This alternates complete forms rather than narrow vertical strips. Lighting, cameras, window apertures, occupied footprints and room layouts were retained for a direct comparison.

Independent architecture and material reviewers compared four actual native drafts (arrival, entry detail, rear terraces and court side) with the preceding outputs. Both found the charcoal bay continuous, the bright strips removed and the brick base/upper finishes coherent around the building. The finish reads taupe-gray in sun and neutral warm gray in shade, without the former bright cream or an obvious pink/yellow/green cast. The supported garage-end infill remains aligned with the wall below. These are scoped appearance findings, not client approval or a claim of photorealism.

### Low study roof: no occupied terrace

The broad edge in the previous images suggested a rooftop patio, but no terrace door or usable deck was modeled. This revision retains a simple unoccupied roof. Its brick upstand is aligned with the wall face below and lowered, with one thin dark coping; the rearward fall and outlet remain. The model has no added furniture, terrace door or guard here. The two existing rear terraces remain the outdoor living spaces.

An occupied roof would be a separate coordinated program change: deliberate upstairs access, a real door/threshold, an upper-plan update, deck construction, guards, waterproofing, drainage and structural design assumptions. The thin current coping is not a guard. Roof membrane/edge technical details remain unresolved.

Remaining presentation limitations include a broad pale vehicle apron, garage/roof-heavy source proportions, schematic site surfaces, sparse low planting and dark lower rear terraces. These are recorded rather than hidden by an illustration. Interior furnishing/trim, dimensional reconciliation and full functional coordination remain open below.

## Verified evidence and its limits

| Evidence | Recorded result | What it does not prove |
|---|---|---|
| [Native reopen receipt](model/native-validation.json) | Blender 4.5.14 LTS reopened the model; 46 library dependencies resolve through relative paths | Suitability, operability or complete installation |
| [Actual asset adoption](model/asset-adoption.json) | All 46 pins match the native libraries and have direct use or a declared adopted parent | Installation performance or operating clearances |
| Evaluated bedroom furniture | Seven bed instances, each resolving to 11 mesh parts; five placed upstairs and two below | Usable room/closet/door clearances, legal bedroom status or emergency escape |
| Brick and openings | 118 local brick meshes carry the physical-meter UV layer; 28 window assemblies exist | Complete material visual acceptance, masonry buildability, selected window performance or correct unscaled product profiles |
| [Opening schedule](model/opening-schedule.json) | 31 facade-opening records across three levels provide positions, sill heights and opening heights | The schedule includes door openings; it is not a count of 31 windows. Each record identifies its opening kind; proposed operation remains unverified |
| Targeted kitchen and envelope checks | Both cooktop glass tops are 5.5 mm above the worktops; upward roof faces and garage setback cap remain; 18 front-bay wall/gable meshes use linked charcoal, the cream link is absent, and low roof fall is 145.7 mm | Full appliance installation, roof weather/structural design or all junction/intersection checks |
| [IFC schema receipt](model/ifc-validation.json) | IFC4, three storeys, zero schema errors | Full semantic/MEP coordination, engineering or permit approval |
| [Bonsai import](model/bonsai-validation.json) | Final IFC reopened with 2,050 mesh objects | Complete semantic building model or specification |
| [Presentation output review](model/output-review.json) | Eight native renders and three furnished level plans inspected and promoted; all are directly embedded in the three README galleries | Complete room usability, construction accuracy or site approval |

## Dimensional discrepancy — open

| Floor | Listing estimate, sq ft | Model floor surface, sq ft | Difference, sq ft |
|---|---:|---:|---:|
| Main | 2,448 | 2,376.474 | -71.526 |
| Upper | 2,180 | 2,482.622 | +302.622 |
| Basement | 2,179 | 2,409.520 | +230.520 |
| Occupied total | **6,807** | **7,268.616** | **+461.616** |

The difference is approximately **6.78%**. The separate garage surface is 974.124 sq ft; model total including garage is 8,242.740 sq ft. The receipt measures horizontal top faces after stair cuts, including walls, excluding terraces/patios/site. These are mesh areas, not surveyed net living areas.

Undimensioned source plans were traced and approximately registered; upper/basement areas were not forced to the listing. The discrepancy is unresolved, not an approved expansion. A measured baseline or defensible recalibration and cross-level alignment review is needed before relying on room lengths, quantities or listing-area fidelity. Proposed floor datums are main 0 m, upper +3.25 m and basement -3.15 m; they are not measured existing elevations.

## Proposed stair and basement changes

[Stair review](model/stair-review.json) records a 1.04 m width for each flight. Foyer and rear main-to-upper stairs each have 19 risers at approximately 171 mm; their centerline goings are approximately 302 mm and 276 mm. Rear basement-to-main has 18 risers at 175 mm and approximately 292 mm centerline going. These are source-generated concept dimensions, not full-path headroom or jurisdictional checks. The 3.15/3.25 m stacked-flight separation is not proof of unobstructed headroom.

The rear basement stair is **relocated into a stacked reservation** beneath the upper flight. The revised rear path starts at (17.05, 7.15) m with a north-facing lower arrival inside the envelope. A targeted authoring check covered 201 rear-flight width samples and landing corners for plan containment; this is not a full 3D clearance/headroom test. The main hall partition was shortened to accommodate the arrival. Original traces and replaced source conditions remain preserved in the authoring source. Original foyer coat/storage partitions and basement stair-storage walls conflicting with these reservations were omitted; under-stair storage and front-entry coat/drop provision still need resolution. West basement lightwells are new daylight/maintenance proposals with retaining and guard geometry; their drainage, structures, access and emergency-escape suitability are unverified.

## Unresolved functional and technical review

- **Daily use:** perform a complete furnished-plan and evaluated-geometry review of entry, parked-car pedestrian access, garage/house connections, bedrooms/wardrobes, baths, dining chairs, billiards cue space and outdoor routes. No comprehensive clear-route or operating-envelope pass is recorded.
- **Doors, windows and appliances:** check full travel/swept envelopes, mounting, thresholds and service/removal paths. Most linked window geometry is scaled in width/height for appearance studies; frame sightlines and handles change with that scaling. Proper size variants and selected products remain necessary. The corrected cooktop/worktop vertical interface passes its targeted native check; other fit, opening and service checks remain outstanding.
- **Program completeness:** primary premium fixtures and both kitchen/laundry equipment sets are modeled, but waste/recycling, complete pantry/general storage, front-arrival coat storage, task/mirror/exterior lighting and door-hardware completeness still need attention. The [program](program.md) records these gaps.
- **Structure/enclosure:** the garage setback cap and roof face orientation are now checked in the native receipt; verify remaining roof/wall/opening details, beams, deck supports, retaining works, snow/wind loads, water paths, insulation and fire separation. Visual geometry supplies none of those calculations.
- **Services and fireplace:** full exhaust/flue, water/drain, HVAC, ventilation, electrical routes and equipment replacement access are not coordinated. Listed existing systems have not been inspected; generic fixtures are not product specifications.
- **Site:** boundary/lot discrepancy, orientation, setbacks, grading, pool barriers/equipment, court clearances, lightwell drainage, retaining structures and planting suitability require site-specific evidence. Existing solar and accessory pool structures remain unmodeled.

## Output and next-review gate

The eight renders and all three furnished plans were inspected as actual pixels, then promoted to stable `outputs/images/` and `outputs/plans/` filenames. The review checked roof/opening consistency, the closed garage setback cap, brick scale/color, terrace/site relationships and visible fixture mounting. Original SVGs accompany the plan PNGs. Interiors remain first furnishing studies, including unfinished trim/reveal junctions; full operating envelopes remain open. The gallery verifier checks registered coverage and direct README embeds separately from visual acceptance.

Regenerate affected native/interchange files and dimension schedules after corrections, then update this review with the checks actually performed. Preserve the listing/model distinction and third-party reference exclusions in [references](references/README.md). Nothing here records an as-built survey, complete home-design pass, selected-product approval, engineering sign-off or permit readiness.
