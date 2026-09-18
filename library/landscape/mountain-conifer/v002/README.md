# Mountain conifer · v002

Original generic mountain evergreen, approximately 46 ft tall. The native collection has connected irregular boughs, branchlets, and individually attached needle geometry; it does not use billboard images or downloaded plant geometry.

- Origin: trunk base at grade, Z up; embedded original bark and needle materials.
- Placement: rotate about Z and use uniform scale 0.78–1.4. Keep trees out of sightlines and locate the trunk base on evaluated terrain.
- Reuse: link the collection in `mountain-conifer.blend`; do not append copies or regenerate one mesh per tree.
- Current real preview: `preview.png`. Fresh-process mesh and dependency check: `validation.json`.
- Geometry and original material rights: CC BY 4.0, attribution Homes project contributors. Authoring code: repository MIT license.

The deterministic generator is `conifer(root, M)` in `tools/mountain05/assets.py`, with `M = mats(root)`. The Mountain build creates missing asset files and links this exact version. The archived v001 generator remains in the same module for reproducibility. Once adopted, v002 must not be edited; publish v003 for subsequent geometry changes.

From the repository root, regenerate the preview and verify the native source in a fresh Blender process:

```sh
Blender --background --python library/landscape/mountain-conifer/v002/render_preview.py
```

This is illustrative vegetation, not a botanical species or planting suitability specification.
