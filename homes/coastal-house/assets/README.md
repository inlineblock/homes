# Coastal asset inventory and adoption schedule

The raised coastal pavilion uses the following pinned shared asset families. The fresh native adoption audit confirms all 38 exact asset versions match the manifest and are actually used, directly or through declared linked parents.

| Component | Shared asset | Version | Adopted use |
| --- | --- | --- | --- |
| Pale oak | `materials/coastal-white-oak` | v001 | Perimeter joinery, interior doors and complementary shared furniture |
| Honed limestone | `materials/coastal-honed-limestone` | v001 | Floors, terrace and retained stone finishes |
| Warm mineral wall finish | `materials/warm-limestone-plaster` | v001 | Interior plaster walls and vault lining |
| Mushroom mineral plaster | `materials/mushroom-mineral-plaster` | v001 | Exterior plaster fields and roof steps |
| Driftwood | `materials/coastal-driftwood` | v001 | Coordinated exposed frames, pergola, eaves, entry/carport timber and island accents |
| Bronze-gray roof metal | `materials/bronze-gray-standing-seam` | v001 | Raised pavilion, lower wings and carport |
| Complementary dark furniture timber | `materials/smoked-oak` | v001 | Retained nested material in shared outdoor furniture; architectural frames use driftwood |
| Oatmeal textile | `materials/woven-oatmeal` | v001 | Shared textile/furniture palette |
| Olive textile | `materials/olive-linen` | v001 | Shared accent cushions and outdoor seating palette |
| Counter stool | `furniture/coastal-oak-counter-stool` | v001 | Island and exterior serving counter |
| Outdoor sofa | `furniture/coastal-outdoor-sofa` | v001 | West terrace conversation group |
| Outdoor lounge chair | `furniture/coastal-outdoor-lounge-chair` | v001 | West terrace conversation group |
| Indoor sofa | `furniture/linen-three-seat-sofa` | v001 | Living-room seating |
| Rounded coffee table | `furniture/oak-rounded-coffee-table` | v001 | Indoor and outdoor conversation groups |
| Eight-foot dining table | `furniture/oak-dining-table-8ft` | v001 | Indoor and terrace dining |
| Dining chair | `furniture/oak-upholstered-dining-chair` | v001 | Indoor and terrace dining |
| Rug | `furniture/woven-oatmeal-rug` | v001 | Living retreat |
| Accent cushion | `furniture/olive-linen-cushion` | v001 | Living-room sofa |
| Opal pendant | `fixtures/opal-globe-pendant` | v001 | Entry lighting |
| Vault-specific linear pendant | `fixtures/lighting-linear-pendant-4ft-vault-3in12` | v001 | Dining light: sloped canopy contact, 90-inch suspension and level four-foot bar |
| Recessed downlight | `fixtures/lighting-recessed-downlight-3in` | v001 | General lighting with ceiling cutouts |
| Task light | `fixtures/lighting-undercabinet-bar-4ft` | v001 | Kitchen preparation lighting |
| Electric fireplace | `fixtures/slim-electric-fireplace-48in` | v001 | Front-service insert in the bespoke living-room limestone surround |
| Tub | `fixtures/freestanding-tub-72in` | v001 | Primary bathroom |
| Toilet | `fixtures/toilet-elongated` | v001 | Both bathrooms |
| Cabinet pull | `hardware/bar-pull-satin-bronze` | v001 | Cabinet and drawer hardware |
| Door lever | `hardware/door-lever-satin-bronze` | v001 | Interior doors |
| Ornamental grass | `landscape/ornamental-grass-clump` | v002 | 170 authored placements in shaped drifts |
| Sage shrub | `landscape/sage-shrub` | v002 | 51 authored placements in shaped drifts |
| Olive tree | `landscape/olive-tree` | v001 | Six authored entry/side/dune framing placements |
| Limestone wall panel | `surfaces/honed-limestone-wall-panel-4x2` | v001 | Full linked 4 x 2 ft facade modules with separately labeled perimeter cuts |
| Limestone paver | `surfaces/honed-limestone-paver-4ft` | v001 | 72 terrace paver instances at 4.02 ft spacing |
| Oak wardrobe | `cabinetry/oak-wardrobe-2ft` | v001 | Fourteen guest/dressing/pantry/coat/linen bays |
| Oven | `appliances/built-in-oven-30in` | v001 | Genuine kitchen appliance bay |
| Dishwasher | `appliances/dishwasher-24in` | v001 | Island equipment bay |
| Induction cooktop | `appliances/induction-cooktop-36in` | v001 | Cooking station |
| Hood | `appliances/wall-hood-36in` | v001 | Cooking ventilation concept |
| Refrigerator | `appliances/panel-ready-fridge-48in` | v001 | Wide integrated refrigeration |

The [adoption audit](../model/asset-adoption.json) verifies these 38 pins against the reopened model. Keep nested material links relative and published versions immutable. Plants permit restrained uniform scale/rotation; furniture, paving, storage and fixtures keep their published dimensions.

The limestone wall-panel family is derived from the shared paver. Full modules remain linked instances; field-edge cuts are host-specific trimmed meshes using the linked stone material and physical texture scale, not stretched panels. Anchor/cavity room, substrate capacity, flashing, drainage and weight are unengineered. The new vault pendant is a published 3:12 sibling of the original linear fixture; its angled contact plates and vertical suspension are not achieved by tilting or scaling the old fixture. The [saved lighting check](../model/lighting-validation.json) verifies native mount contact, beam separation and a level 8.55 ft light bar.

The sofa, lounge chair and textile additions are reusable library families. Site-specific geometry remains local: house layout, sliding pockets, full-width serving cabinetry, pergola, entry canopy, low terrace screen, dune terrain, original wall-art composition and the living sofa's fitted chaise extension. The original unbranded passenger cars reuse `tools/garage03/cars.py`.

Material and furniture appearance is concept geometry. Outdoor deployment does not establish moisture, UV, corrosion, fire or structural ratings. Plant forms do not identify a verified coastal species selection. Final products and site conditions require selection and review.

Original designs/assets: CC BY 4.0, attribution Homes project contributors. Authoring code: MIT.

The current facade uses **ten full linked panels and 31 separately labeled perimeter cuts**. Both types retain the same limestone material and nominal thickness. Driftwood, roof metal, wall-panel and vault-pendant assets are new reusable variations; the other 33 pins reuse existing versions.

Current host visual review uses the native terrace, serving-counter, great-room and exposed-vault views: architectural driftwood reads as a coordinated gray-brown family in sun and shade, with grain along the actual members; bronze-gray roofing has restrained highlights; the limestone field uses visible large-format joints. Isolated library receipts describe the reusable asset, while this home records its actual adoption and geometry checks. Final fastening, weatherproofing and listed-product performance remain unresolved.

The new electric insert is an original shared concept, freshly linked and previewed before host adoption. Its limestone surround is bespoke to the 5.455 ft pocket-wall width; it uses the existing pinned limestone material. The host check confirms an actual recess, rear service reservation, 3 ft front-removal volume, 3.05 ft to the chaise and no sliding-panel collision at seven frames. This is geometry evidence, not a selected electrical appliance installation.
