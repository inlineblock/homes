# Garage Loft 03 asset-use schedule

This schedule reconciles [project.json](../project.json), the [home generator](../../../tools/garage03/build.py), [asset generator](../../../tools/garage03/assets.py) and existing [model validation](../model/model-validation.json). The receipt lists six relative libraries. Uses below come from source and existing records; this documentation pass did not freshly reopen the native scene or verify placements, operation or rendered appearance.

| Exact asset and version | Contribution history | Source-defined placement/use |
| --- | --- | --- |
| [materials/warm-vertical-cedar · v002](../../../library/materials/warm-vertical-cedar/v002/asset.json) | Revised shared finish adopted for this garage | Upper exterior boards and entry timber |
| [materials/charcoal-standing-seam · v001](../../../library/materials/charcoal-standing-seam/v001/asset.json) | Reused existing material | Fitted roof and seam geometry |
| [fixtures/opal-globe-pendant · v001](../../../library/fixtures/opal-globe-pendant/v001/asset.json) | Reused Atrium-derived asset | Two original pendants over the pool table |
| [furniture/walnut-counter-stool · v001](../../../library/furniture/walnut-counter-stool/v001/asset.json) | Reused Atrium-derived asset | Three refreshments-counter stools |
| [fixtures/double-pit-parking-carriage · v002](../../../library/fixtures/double-pit-parking-carriage/v002/asset.json) | Garage contribution, revised wheel-stop placement | One linked moving double-width carriage, shown in stored/raised states |
| [furniture/walnut-eight-foot-pool-table · v002](../../../library/furniture/walnut-eight-foot-pool-table/v002/asset.json) | Garage contribution, refined playing surface/finish | Upstairs game-room table |

These are the six manifest pins. Their manifests declare no external library dependencies. Preserve earlier versions for other homes; never overwrite these adopted binaries. Original assets use CC BY 4.0 with attribution to Homes project contributors, and code uses MIT. The carriage is an original schematic proxy, not manufacturer CAD or certified equipment; see [planning references](../references/README.md).

## Local geometry and migration debt

The pit/foundation, garage slabs and stair opening, roof/cladding layout, doors, fixed operator apron and equipment-specific guide/guard reservations are fitted to this concept. The lift's separate fixed guides, control pedestal and front enclosure are local schematic interfaces, not part of the linked carriage or a resolved safety system.

Cars reuse [the original coupe generator](../../../tools/garage03/cars.py), but are local generated meshes, not library collection adoption. This is shared authoring code only. Promote a reviewed vehicle asset if adopting this geometry across homes, with honest vehicle-envelope and operating limits.

The lounge sofa/rug/coffee table, media credenza, refreshments cabinet modules, gaming desk, cue rack, architectural light details, heat-pump proxies, garden plants and entry pavers also remain local. Existing furniture, lighting, cabinetry, planting and paving families should be evaluated on the next coordinated revision. Fit-dependent sizing may call for a new reusable sibling; it does not justify silently copying generic components forever. HVAC proxies must remain labeled unsized until actual systems design exists.

Local plaster, concrete, walnut, upholstery, glazing, metal and vehicle-paint shaders are not additional shared material pins. Review appropriate material options rather than inferring reuse from matching colors.

Before adopting replacements, preserve the pool cue envelope, fixed-floor walking routes, lift clearances and stair access; verify the host, update this schedule/manifest, and refresh affected plans and images. See [design-review.md](../design-review.md) and [the contribution workflow](../../../docs/assets.md).
