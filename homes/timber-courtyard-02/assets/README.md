# Timber Courtyard 02 asset-use schedule

The promoted kitchen/pantry revision adopts **25 direct pinned assets and two additional transitive dependencies**. These are actual linked components and materials, not a list of unused library options. The [project manifest](../project.json), [kitchen source](../../../tools/timber02/kitchen.py), retained roof and native model define this schedule.

Independent [kitchen validation](../model/kitchen-validation.json) records 31 checks: zero geometry/planning failures and one unresolved selected-product allowance. It covers full-scale equipment, relative links, actual openings/cavities, sampled operation, pantry access and grounded furniture. See the [design review](../design-review.md) for scope and limitations; this is not whole-home approval.

## Direct pinned assets

| Exact asset/version | Actual role |
| --- | --- |
| [materials/smoked-oak · v001](../../../library/materials/smoked-oak/v001/asset.json) | Cabinet/appliance finish, fitted fillers, island back/ends and pantry door; physical-meter timber UVs |
| [materials/coastal-honed-limestone · v001](../../../library/materials/coastal-honed-limestone/v001/asset.json) | Exact-fit kitchen/pantry worktops and low splash |
| [materials/warm-vertical-cedar · v001](../../../library/materials/warm-vertical-cedar/v001/asset.json) | Retained exterior/structure, fitted kitchen/pantry ceiling and wall infill |
| [cabinetry/smoked-oak-drawer-base-2ft · v001](../../../library/cabinetry/smoked-oak-drawer-base-2ft/v001/asset.json) | Four rear kitchen bases, three island bases, one cooking landing and three pantry bases |
| [cabinetry/smoked-oak-sink-base-36in · v001](../../../library/cabinetry/smoked-oak-sink-base-36in/v001/asset.json) | Open sink/plumbing cavity under the garden-facing sink |
| [cabinetry/smoked-oak-oven-base-36in · v001](../../../library/cabinetry/smoked-oak-oven-base-36in/v001/asset.json) | Actual open east-wall oven housing |
| [cabinetry/smoked-oak-waste-pullout-18in · v001](../../../library/cabinetry/smoked-oak-waste-pullout-18in/v001/asset.json) | Island waste/recycling pullout with two bins |
| [appliances/smoked-oak-panel-ready-fridge-48in · v001](../../../library/appliances/smoked-oak-panel-ready-fridge-48in/v001/asset.json) | Full-size integrated refrigeration envelope, doors, pulls and grille |
| [appliances/smoked-oak-panel-ready-dishwasher-24in · v001](../../../library/appliances/smoked-oak-panel-ready-dishwasher-24in/v001/asset.json) | Integrated dishwasher west of sink; open door/operator beyond island west edge |
| [appliances/induction-cooktop-36in · v001](../../../library/appliances/induction-cooktop-36in/v001/asset.json) | Five-zone cooking with an actual underbody opening |
| [appliances/built-in-oven-30in · v001](../../../library/appliances/built-in-oven-30in/v001/asset.json) | Full-size oven in an open housing; sampled door/operator clearance |
| [appliances/wall-hood-36in · v001](../../../library/appliances/wall-hood-36in/v001/asset.json) | Extraction canopy and filter; host supplies fitted riser toward roof |
| [fixtures/kitchen-sink-mixer-650 · v002](../../../library/fixtures/kitchen-sink-mixer-650/v002/asset.json) | Real bowl/mixer; v002 corrects host opening to 664 × 464 mm without changing v001 geometry |
| [materials/sage-fluted-tile · v001](../../../library/materials/sage-fluted-tile/v001/asset.json) | Shared tile collections concentrated on the cooking wall |
| [furniture/walnut-counter-stool · v001](../../../library/furniture/walnut-counter-stool/v001/asset.json) | Three island seats at 30 in centers |
| [cabinetry/smoked-oak-pantry-shelf-2ft · v001](../../../library/cabinetry/smoked-oak-pantry-shelf-2ft/v001/asset.json) | Six 24in-wide, 12in-deep, 84in-high pantry modules |
| [fixtures/lighting-recessed-downlight-3in · v001](../../../library/fixtures/lighting-recessed-downlight-3in/v001/asset.json) | Seven kitchen/pantry fixtures with ceiling openings and host-owned lights |
| [fixtures/opal-globe-pendant · v001](../../../library/fixtures/opal-globe-pendant/v001/asset.json) | Retained dining showpiece |
| [fixtures/lighting-linear-pendant-4ft · v001](../../../library/fixtures/lighting-linear-pendant-4ft/v001/asset.json) | Island showpiece with fitted upper suspension/support |
| [fixtures/duplex-power-outlet-bronze · v001](../../../library/fixtures/duplex-power-outlet-bronze/v001/asset.json) | Two garden-counter points, one pantry-counter point, one island-end point; only declared fixture collection instanced |
| [furniture/oak-upholstered-dining-chair · v001](../../../library/furniture/oak-upholstered-dining-chair/v001/asset.json) | Six supported dining chairs replacing legless proxies |
| [furniture/oak-rounded-coffee-table · v001](../../../library/furniture/oak-rounded-coffee-table/v001/asset.json) | Supported coffee table replacing local unsupported top |
| [furniture/linen-three-seat-sofa · v001](../../../library/furniture/linen-three-seat-sofa/v001/asset.json) | Grounded shared living-room sofa |
| [furniture/oak-dining-table-8ft · v001](../../../library/furniture/oak-dining-table-8ft/v001/asset.json) | Grounded shared dining table replacing local floating leg assembly |
| [materials/charcoal-standing-seam · v001](../../../library/materials/charcoal-standing-seam/v001/asset.json) | Retained roof surfaces and raised seams |

## Transitive dependencies and contribution history

- [materials/coastal-white-oak · v001](../../../library/materials/coastal-white-oak/v001/asset.json) is the pinned finish inside reused adjacent furniture. Those adopted collections were not silently recolored.
- [hardware/bar-pull-satin-bronze · v001](../../../library/hardware/bar-pull-satin-bronze/v001/asset.json) supplies linked cabinet handles and the outlet's pinned bronze material.
- The smoked-oak 24 in drawer base derives from the actual `cabinetry/oak-drawer-base-2ft/v001`; sink, oven, waste and pantry modules are new original components. Their [publisher](../../../tools/library/build_timber_kitchen_cabinets.py) preserves the parent and verifies fresh links, meter UVs and component interfaces.
- Smoked-oak refrigerator/dishwasher variants derive from the existing full-size panel-ready fridge and stainless dishwasher. Their manifests identify the actual parents and changes; no appliance was shrunk to fit.
- Sink v002 corrects the original undersized metadata opening: actual outer bowl walls measure 654 × 454 mm, so the host opening is 664 × 464 mm, adding 5 mm each side. Geometry equality with v001 was checked and v001 remains intact.

Original assets use CC BY 4.0 with attribution to Homes project contributors; authoring code uses MIT. Preserve separate [user-reference restrictions](../references/README.md). Appliances and fixtures are original concept components, not specified or certified commercial products.

## Host-specific geometry and remaining migration debt

Exact-fit worktops/cutouts, fillers/end cheeks, island back/supports, service cover, ceiling lining/openings/suspension, exhaust riser, pantry door/opening, anti-tip ledger, wall infill/clerestory and power recesses follow this home's dimensions and remain local. Courtyard geometry, fitted roof/gable/truss, entry canopy and garden boundaries remain local for the same reason. This does not make repeated furniture, plants or fixtures bespoke.

Beds, bedside furniture, bathroom proxies, some local material recipes, garden plants and repeated stepping slabs still need library migration and coordinated review. Local planting made by a common helper is not linked asset adoption. Complete bedroom storage, bathroom/laundry provision, site parking and building services remain open in the design review.
