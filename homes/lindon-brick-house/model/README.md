# Editable source and regeneration

`lindon-brick-house.blend` is the furnished visualization source. The IFC is classified concept geometry, including linked window meshes; it is not a complete BIM specification. Native and IFC validation receipts live beside the files. Current native renders use 2400 × 1600 pixels and 320 Cycles samples; appearance critiques are recorded separately in the design review.

The geometric source is [design.py](../../../tools/lindon06/design.py). It preserves nondimensioned source traces separately from proposed stair coordination. [openings.py](../../../tools/lindon06/openings.py) drives both wall apertures and drawings. Site, envelope, interiors and stairs have separate authoring modules. All use meters; drawings display feet/inches.

Run from the repository root, substituting your Blender executable. Blender 4.5.14 LTS and Bonsai 0.8.5 were used. Drawing generation needs Python and Pillow.

```sh
blender --background --python tools/lindon06/build.py
blender --background --python tools/lindon06/verify.py
blender --background homes/lindon-brick-house/model/lindon-brick-house.blend --python tools/lindon06/render.py -- --samples 320
python3 tools/lindon06/draw.py
blender --background homes/lindon-brick-house/model/lindon-brick-house.blend --python tools/common/export_scene_ifc.py
blender --background --python tools/common/verify_bonsai.py -- lindon-brick-house
python3 tools/common/verify_galleries.py
```

**Build overwrites the native model and source receipts.** Preserve manual edits in Git first. Rendering and drawing write drafts to ignored `outputs/work/`. Inspect every affected image/plan before copying it to the corresponding stable path in `outputs/images/` or `outputs/plans/`, then update README/gallery records together. Never publish third-party listing photographs or the downloaded floor-plan images.

The source floor areas differ from the listing and are explicitly recorded in `native-validation.json`. Reconcile with measured drawings before making dimensional decisions. `stair-review.json` describes the proposed flights; its centerline dimensions are not evidence of jurisdictional or structural approval.
