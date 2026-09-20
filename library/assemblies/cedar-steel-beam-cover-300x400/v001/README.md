# Cedar-look steel beam cover — 300 × 400 mm

![Native preview](preview.png)

Original nonstructural three-sided cover, with actual 20 mm finish panels and an open cavity. The finish suggests cedar; steel, fastening, fire protection and selected wood-look product remain host responsibilities. This is not a structural timber beam.

- Native stock: **1 m long × 300 mm wide × 400 mm high**.
- Local X is length; Y is section width; bottom exposed face is Z = 0. Open top faces +Z.
- Link collection `Hollow cedar-look steel beam cover 300x400 | v001` from [the native asset](cedar-steel-beam-cover-300x400.blend).
- Local X scaling is permitted from 1 to 7.3152 m installed length; Y and Z stay exactly 1. Rotate the complete instance to match the beam direction/pitch. No thickness/section scaling.
- Cavity is Y ±130 mm, Z 20–400 mm. A concept 10 mm allowance gives steel envelope Y ±120 mm, Z 30–390 mm. These are geometric allowances, not an engineered section selection.
- Cut ends stay open; home-specific terminations, concealed brackets, tolerances, movement, insulation/fire protection and weather protection must be resolved separately.
- Reuses [warm cedar v003](../../../materials/warm-vertical-cedar/v003/asset.json). Cross-grain scale stays fixed under length scaling; longitudinal grain features elongate. Publish a length-specific sibling with regenerated meter UVs when exact longitudinal grain scale is required.

Fresh native reopen, linked dependency resolution, dimensions, 20 mm thickness and seven cavity ray checks passed. The actual native preview was visually inspected. [Validation record](validation.json). Host integration is checked in the adopting home, not inferred from this isolated preview.

Generator: `tools/library/publish_timber_beam_cover.py`. Original Homes project contributors asset, CC BY 4.0. Authoring code MIT.
