# Marsh grapefruit trees

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| marsh-young | `grapefruit_tree__marsh_young` | 2.73 × 2.72 × 3.56 | 2.73 × 2.72 × 3.56 m |
| marsh-spreading | `grapefruit_tree__marsh_spreading` | 4.79 × 4.54 × 4.62 | 4.79 × 4.54 × 4.62 m |
| marsh-clusters | `grapefruit_tree__marsh_clusters` | 4.05 × 4.12 × 3.62 | 4.05 × 4.12 × 3.62 m |

## Source and use

Generator: `tools/library/plants/citrus.py`. Regeneration command is recorded in `asset.json`.

The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.

CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.

Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.

Fruit clusters use 1–5 separate fruits at different twig nodes, ±15% nominal-size variation and at least 4 mm separation between conservative fruit sphere envelopes. This geometric clearance is checked during generation.

<!-- native-review -->
## Native visual review

![Three editable plant variants](preview.png)

![Actual modeled detail](detail.png)

Corrected clusters show staggered depth, varied fruit counts and sizes, and irregular spacing; repeated triangular triplets are resolved. Whole crowns remain dense and grounded with attached branching. Smooth peel and geometric leaf edges remain close-up limitations.

Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in [validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; no existing home adoption is claimed.
