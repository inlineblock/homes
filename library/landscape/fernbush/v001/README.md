# Fernbush

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| young-lacy | `fernbush__young-lacy` | 0.91 × 0.94 × 0.67 | Young open lacy shrub with twice-divided fern-like foliage. |
| mature-white-bloom | `fernbush__mature-white-bloom` | 1.77 × 1.76 × 1.52 | Spreading mature shrub with many white terminal panicles and lacy foliage. |
| winter-structure | `fernbush__winter-structure` | 1.13 × 1.26 × 1.26 | Sparse winter branching shrub with reduced dry foliage and spent panicles. |

## Source and use

Generator: `tools/library/plants/xeric.py`. Regeneration command is recorded in `asset.json`.

The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.

CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.

Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.

<!-- native-review -->
## Native visual review

![Three editable plant variants](preview.png)

![Actual modeled detail](detail.png)

Distinct grass, cushion, shrub and flowering silhouettes. Whole plants and details show adequate density and attachment. Flower mouths, seedheads and leaf edges remain geometric at macro scale.

Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in [validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; no existing home adoption is claimed.
