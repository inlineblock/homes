# Timber Courtyard 02 asset-use schedule

This schedule is a documentation reconciliation of [project.json](../project.json), the [generator](../../../tools/timber02/build.py) and existing [native-model receipt](../model/model-validation.json). That receipt lists five relative libraries. The uses below are source-defined; no new native reopen, placement-count audit, functional check or visual review was performed for this schedule.

| Exact asset and version | Contribution history | Source-defined placement/use |
| --- | --- | --- |
| [materials/sage-fluted-tile · v001](../../../library/materials/sage-fluted-tile/v001/asset.json) | Reused Atrium contribution | Linked kitchen backsplash tiles |
| [fixtures/opal-globe-pendant · v001](../../../library/fixtures/opal-globe-pendant/v001/asset.json) | Reused asset promoted from Atrium | Dining and island pendants |
| [furniture/walnut-counter-stool · v001](../../../library/furniture/walnut-counter-stool/v001/asset.json) | Reused asset promoted from Atrium | Kitchen island stools |
| [materials/warm-vertical-cedar · v001](../../../library/materials/warm-vertical-cedar/v001/asset.json) | Original material contribution for this home | Individually generated cladding boards, exposed timber and selected interior pieces |
| [materials/charcoal-standing-seam · v001](../../../library/materials/charcoal-standing-seam/v001/asset.json) | Original material contribution for this home | Locally fitted roof surfaces and standing-seam geometry |

These five versions are the complete manifest pin set. Their manifests declare no additional external library dependencies. Material links do not make the fitted board/roof assemblies reusable collections. Keep adopted versions immutable and links relative. Original content is CC BY 4.0, attribution Homes project contributors; authoring code is MIT. The user reference has separate restrictions in [reference notes](../references/README.md).

## Local repeated components and migration debt

- Dining chairs, coffee table, sofa, beds and bedside tables remain local. The existing gallery receipt documents missing dining-chair legs and a missing coffee-table base. Evaluate current shared furniture or contribute fit-appropriate variations; these defects are unresolved, not intentional bespoke exceptions.
- Kitchen bases, island, refrigeration/hob/sink proxies and bathroom fixtures are local. A modeled oven and hood are absent according to the existing review. Select the missing complete equipment set and coordinated hardware from the library before treating the interior as resolved.
- Courtyard and garden trees, shrubs, grasses and rocks use common generation helpers but are local meshes. Search existing landscape families and publish any genuinely missing plant form. Repeated stepping slabs also need a suitable shared module or new dimensional variation; their placement alone is not a bespoke exemption.
- Other local material recipes are not additional library pins. Compare their physical scale and palette to available material families when migrating.

The courtyard footprint, wing partitions/glazing, fitted roof/gable/truss assembly, entry canopy, garden-bed boundaries and exact-fit worktops stay local because they follow this home's dimensions. Fix layout/fit first, then adopt reviewed assets, update the manifest/schedule and affected outputs. See [design-review.md](../design-review.md) and [contribution rules](../../../docs/assets.md).
