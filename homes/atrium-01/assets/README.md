# Atrium 01 asset-use schedule

This documentation audit reconciles [project.json](../project.json) with the [kitchen generator](../../../tools/atrium01/kitchen.py) and [home generator](../../../tools/atrium01/build.py). It does not record a fresh native reopen, placement count, operating-clearance test or visual review. The existing [gallery receipt](../model/gallery-validation.json) covers the earlier camera-only work; the [design review](../design-review.md) retains unresolved legacy design conditions.

| Exact asset and version | Contribution history | Source-defined use | Evidence status |
| --- | --- | --- | --- |
| [materials/sage-fluted-tile · v001](../../../library/materials/sage-fluted-tile/v001/asset.json) | Original contribution from this home; retained pinned version | Linked tile collection instantiated across the kitchen backsplash | Declared in the home manifest and linked by `tile_library`; no fresh adoption audit in this documentation pass |

The tile manifest declares no external library dependencies. Preserve its version and repository-relative native link. Original project assets use CC BY 4.0 with attribution to Homes project contributors; authoring code uses MIT.

## Local repeated components and migration debt

The generator still builds kitchen stools and opal pendants locally. Their promoted [walnut stool](../../../library/furniture/walnut-counter-stool/v001/asset.json) and [opal pendant](../../../library/fixtures/opal-globe-pendant/v001/asset.json) are shared by later homes; **promotion did not migrate Atrium's own instances**. They are candidate replacements, not additional adopted pins.

The following are also local generated geometry or materials, not linked library reuse:

- Kitchen cabinet modules, appliances, sink/tap, pulls and dining lighting; compare the current cabinetry, appliance, hardware and fixture families before a coordinated equipment revision.
- Beds, bedside tables, dining chairs/table, sofa, coffee table and rugs; evaluate current furniture dimensions and finishes, publish genuine missing variations, then explicitly adopt them.
- Bathroom vanities, basins, toilets, showers and laundry proxies; select compatible shared options and resolve their host openings/services/operating space.
- Atrium trees/planting, stepping slabs and local stone, timber, metal, glass and textile shaders; repeated planting and paving need library options or reviewed contributions. A shared generator alone does not satisfy adoption.

The fitted building footprint, atrium opening, walls/glazing, roof and beam layout, terrace slab and exact-fit kitchen worktops remain local because their dimensions and intersections depend on this home. That does not exempt standard furniture, plants or equipment from migration.

Before replacing any local family, verify fit and circulation in the native model, preserve adopted versions, update the manifest and this schedule, and regenerate affected plans/renders and photographic studies. The backlog is unresolved work, not a claim that the current home meets every newer repository standard. Follow [the contribution workflow](../../../docs/assets.md).
