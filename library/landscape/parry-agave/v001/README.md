# Parry’s agave

Original illustrative botanical geometry; not a certified species identification, nursery specification, or climate suitability approval.

Original editable mesh asset, in meters with Z up and the plant base at the origin.

## Collections

Link one collection from the Blender file for each planting instance; variants share the same origin intentionally.

| Variant | Collection | Modeled size (W × D × H, m) | Description |
|---|---|---|---|
| compact-rosette | `parry_agave__compact_rosette` | 1.68 × 1.55 × 0.56 | Compact powder-blue fleshy rosette |
| offset-colony | `parry_agave__offset_colony` | 2.21 × 2.25 × 0.67 | Mature rosette with four smaller offsets |
| flowering-stalk | `parry_agave__flowering_stalk` | 2.04 × 1.88 × 4.00 | Mature terminal flowering rosette and branched stalk |

## Source and use

Generator: `tools/library/plants/desert.py`. Regeneration command is recorded in `asset.json`.

The generator permits rebuilding this candidate while untracked. Once versioned, publish a new version rather than modifying this one.

CC BY 4.0; attribution: Homes project contributors. All geometry and procedural materials are original.

Choose variants by modeled size and state. These dimensions are not expected mature spread; consult the selection notes for site limitations. A library model does not establish host adoption.

<!-- native-review -->
## Native visual review

![Three editable plant variants](preview.png)

![Actual modeled detail](detail.png)

Rosette and offset forms are distinct. Flowering stalk has flared flower mouths and stamens; floral branching remains somewhat regular at close range.

Reviewed for architectural concept landscape use. Close views retain simplified botanical geometry and procedural surfaces; these are not photographic macro plants. Native reopen, measured bounds and fresh linked instances are recorded in [validation.json](validation.json). The [comparative nursery](../../nursery/README.md) tests shared placement; no existing home adoption is claimed.
