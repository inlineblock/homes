# Shared asset catalog

All current assets are original project work and versioned as `v001`. Keep versions stable once a home references them.

| Asset | Category | Placement / scale | Used by |
|---|---|---|---|
| [Sage fluted ceramic](materials/sage-fluted-tile/v001/asset.json) | Material + tile geometry | 3 × 12 in nominal module, including grout | Atrium 01, Timber Courtyard 02 |
| [Opal globe pendant](fixtures/opal-globe-pendant/v001/asset.json) | Fixture collection | Origin at ceiling mount; geometry extends down | Promoted from Atrium 01; linked by Timber Courtyard 02 |
| [Walnut counter stool](furniture/walnut-counter-stool/v001/asset.json) | Furniture collection | Floor origin under seat; approx. 24.6 in seat height | Promoted from Atrium 01; linked by Timber Courtyard 02 |
| [Warm vertical cedar](materials/warm-vertical-cedar/v001/asset.json) | Procedural material | Intended for 6 in board modules | Timber Courtyard 02 |
| [Charcoal standing-seam metal](materials/charcoal-standing-seam/v001/asset.json) | Procedural material | Intended for 12 in seam spacing | Timber Courtyard 02 |

Open or link the `.blend` file next to each manifest. Tile and fixture assets are collections; cedar and metal are material datablocks. The material assets do not generate geometry by themselves: reusable geometry helpers and the home's generator create the matching boards and seams.

The procedural planting helpers in `tools/common/landscape.py` are another reusable source artifact. They generate trees, shrubs, grasses, and boulders at explicit physical sizes with deterministic seeds.

Read [asset conventions](../docs/assets.md) before adding or changing an asset. Preserve local coordinates when linking collections, especially curve-based objects.

## Garage Loft additions

- [Double pit parking carriage](fixtures/double-pit-parking-carriage/v001/asset.json): original two-level, double-width schematic equipment proxy. References KLAUS planning dimensions; not manufacturer CAD or installation documentation.
- [Walnut eight-foot pool table](furniture/walnut-eight-foot-pool-table/v001/asset.json): original furniture with a 44 x 88 inch playing area.
