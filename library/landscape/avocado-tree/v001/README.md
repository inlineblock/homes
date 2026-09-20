# Avocado tree

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| young-orchard | `avocado-tree__young-orchard` | 2.32 × 2.38 × 2.31 | Young single-leader orchard tree, vegetative |
| maintained-garden | `avocado-tree__maintained-garden` | 3.86 × 3.91 × 3.75 | Maintained garden crown with attached fruit |
| mature-fruiting | `avocado-tree__mature-fruiting` | 5.19 × 5.11 × 5.36 | Large spreading mature fruiting crown |

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
