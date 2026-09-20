# Kinnikinnick / common bearberry

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| small-mat | `Kinnikinnick_small_mat` | 0.96 × 1.01 × 0.22 | Small leathery evergreen mat |
| broad-mat | `Kinnikinnick_broad_mat` | 1.76 × 1.70 × 0.22 | Wide irregular prostrate branching groundcover |
| berry-edge | `Kinnikinnick_berry_edge` | 1.14 × 1.19 × 0.21 | Asymmetric berry-bearing rock-edge patch |

## Source and use

Generator: `tools/library/plants/mountain.py`. Regeneration command is recorded in `asset.json`.

The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.

CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.

Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.

<!-- native-review -->
## Native visual review

![Three editable plant variants](preview.png)

![Actual modeled detail](detail.png)

Distinct seasonal and growth forms, continuous leafy crowns where appropriate, grounded bases and connected visible detail. Finer leaf edges and bark microdetail remain simplified.

Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in [validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; no existing home adoption is claimed.
