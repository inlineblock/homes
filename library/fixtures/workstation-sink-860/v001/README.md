# Stainless workstation sink · v001

![Actual native installation study](preview.png)

Original, dimensioned concept geometry. The preview uses the published native asset in a real cutout study; the plain studio supports are not a cabinet supplied by this package. No home has adopted this version yet.

The inner top bowl is **860 × 450mm**, 250mm deep. The flange is 910 × 500mm. A continuous formed shell slopes into an actual 90mm drain opening and hollow 36mm-bore tailpiece; the basin has no opaque bottom cap.

Use the bowl center as XY=0 and finished countertop top as Z=0; front is −Y. The flange top sits at Z=−38.1mm. The pinned shared pull-down faucet is centered at **(0, 285mm)** with its own 35mm deck bore. This package targets a 38.1mm worktop: do not change thickness by moving the entire combined sink/faucet collection. Instead coordinate separate sink/faucet placements or publish a thickness variant. Rigid translation and rotation only; do not stretch the asset.

The worktop through-opening is **870 × 460mm**, with 25mm concept corner radius and 5mm positive reveal per side relative to the inner bowl. The example top is 780mm deep centered at Y=50mm, with a separate faucet bore. Final fabrication requires the selected product template, mounting brackets and sealant system.

The removable 310×438×25mm oak board rests on actual ledges at Z=−57mm. A separate open stainless rod mat sits to the right, leaving the center accessible. Move/remove both for large pots and cleaning. Food-contact, heat and load ratings are unverified. The board links `materials/coastal-white-oak/v001`; it is not a home-local copied finish.

**Cabinet not supplied.** A nominal 42-inch base is only a planning minimum. Require at least 930mm clear width, the full flange and sloping bowl volume below the top, and separate faucet stem/nut/hose space. The manifest records exact keep-outs. Keep drawers, shelves and upper rails out of these volumes. The suggested cabinet origin is Y=45mm relative to the bowl; this requires a coordinated sink-specific frame.

Reserve 800mm in front for standing, with separate circulation as required. Trap, disposal, connectors, water services, waterproofing and sound support are not included. Sink/counter/faucet heat, wet, chemical and food-contact performance remain unverified pending selected products and installation details.

The Blender source, manifest and fresh-open receipt are alongside this README. All geometry and procedural finishes are original Homes project work or explicitly derived from the repository versions listed in the manifest. CC BY 4.0; attribute Homes project contributors. No manufacturer CAD or restricted source imagery is included.

Reproduce from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --asset workstation-sink-860
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --verify --render --asset workstation-sink-860
```

The generator preserves existing native files. Use a new version after adoption; never overwrite pinned assets. Verification reopens, resolves relative dependencies, checks native dimensions and open bowl/drain geometry, then produces the actual CPU preview. Render inspection passes for the visible function and openings, while home integration remains unchecked.
