# Lindon Brick House — first concept review

**Disposition: editable first concept; not a resolved design.** Recorded checks establish a reusable native model and selected geometric facts. Dimensional reconciliation and full functional coordination remain open. The user's approved direction is warm modern red brick with an old-school character and improved rectangular windows; farmhouse styling was superseded.

## Verified evidence and its limits

| Evidence | Recorded result | What it does not prove |
|---|---|---|
| [Native reopen receipt](model/native-validation.json) | Blender 4.5.14 LTS reopened the model; 43 library dependencies resolve through relative paths | Suitability, operability or complete installation |
| [Actual asset adoption](model/asset-adoption.json) | All 43 pins match the native libraries and have direct use or a declared adopted parent | Installation performance or operating clearances |
| Evaluated bedroom furniture | Seven bed instances, each resolving to 11 mesh parts; five placed upstairs and two below | Usable room/closet/door clearances, legal bedroom status or emergency escape |
| Brick and openings | 189 local brick meshes carry the physical-meter UV layer; 28 window assemblies exist | Complete material visual acceptance, masonry buildability, selected window performance or correct unscaled product profiles |
| [Opening schedule](model/opening-schedule.json) | 31 facade-opening records across three levels provide positions, sill heights and opening heights | The schedule includes door openings; it is not a count of 31 windows. Each record identifies its opening kind; proposed operation remains unverified |
| Targeted kitchen and envelope checks | Both cooktop glass tops are 5.5 mm above the worktops; roof faces point upward with thickness beneath the visible surfaces; garage setback cap exists and excludes the upper occupied footprint | Full appliance installation, roof weather/structural design or all junction/intersection checks |
| [IFC schema receipt](model/ifc-validation.json) | IFC4, three storeys, zero schema errors | Full semantic/MEP coordination, engineering or permit approval |
| [Bonsai import](model/bonsai-validation.json) | Final IFC reopened with 2,451 mesh objects | Complete semantic building model or specification |
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

The eight renders and all three furnished plans were inspected as actual pixels, then promoted to stable `outputs/images/` and `outputs/plans/` filenames. The review checked roof/opening consistency, the closed garage setback cap, brick scale/color, terrace/site relationships and visible fixture mounting. Original SVGs accompany the plan PNGs. Interiors remain first furnishing studies; full operating envelopes remain open. The gallery verifier checks registered coverage and direct README embeds separately from visual acceptance.

Regenerate affected native/interchange files and dimension schedules after corrections, then update this review with the checks actually performed. Preserve the listing/model distinction and third-party reference exclusions in [references](references/README.md). Nothing here records an as-built survey, complete home-design pass, selected-product approval, engineering sign-off or permit readiness.
