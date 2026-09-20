# Pomegranate

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| natural-shrub | `pomegranate-tree__natural-shrub` | 3.35 × 3.22 × 2.39 | Natural multi-stem leafy shrub |
| flowering-standard | `pomegranate-tree__flowering-standard` | 3.24 × 3.09 × 2.76 | Single-trunk trained tree with red tubular flowers |
| fruit-loaded | `pomegranate-tree__fruit-loaded` | 3.34 × 3.37 × 2.62 | Maintained multi-stem ripe fruit crown |

## Source and use

Generator: `tools/library/plants/orchard.py`. Regeneration command is recorded in `asset.json`.

The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.

CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.

Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.

<!-- native-review -->
## Native visual review

![Three editable plant variants](preview.png)

![Actual modeled detail](detail.png)

Fuller natural crowns and distinct trained, fruiting or dormant forms. Broad avocado leaves, lobed fig foliage, pomegranate calyces and apple espalier are visible. Fruit surfaces and branching retain concept-level simplification.

Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in [validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; no existing home adoption is claimed.
