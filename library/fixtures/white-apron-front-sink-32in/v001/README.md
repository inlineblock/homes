# White apron-front sink · v001

![Actual native installation study](preview.png)

Original, dimensioned concept geometry. The preview uses the published native asset in a real cutout study; the plain studio supports are not a cabinet supplied by this package. No home has adopted this version yet.

The inner top bowl is **742.8 × 428.8mm**, 255mm deep. The flange is 812.8 × 498.8mm. A continuous formed shell slopes into an actual 90mm drain opening and hollow 36mm-bore tailpiece; the basin has no opaque bottom cap.

Use the bowl center as XY=0 and finished countertop top as Z=0; front is −Y. The flange top sits at Z=−38.1mm. The pinned shared pull-down faucet is centered at **(0, 310mm)** with its own 35mm deck bore. This package targets a 38.1mm worktop: do not change thickness by moving the entire combined sink/faucet collection. Instead coordinate separate sink/faucet placements or publish a thickness variant. Rigid translation and rotation only; do not stretch the asset.

The countertop uses a **stepped U-opening**. Behind the apron, side edges are X=±376.4mm and the rear edge is Y=219.4mm. At Y=−214.4mm the opening widens to X=±411.4mm and continues through the front edge. This preserves support over the bowl flange while allowing the 812.8mm apron through the front. Seal the 5mm side seams with a selected compatible system; final fabrication radii must come from real product templates. The actual preview corrects the initial overly large rear cutout.

The white finish is an original glazed appearance over a concept shell, not a specified fireclay product or claimed wall thickness. Provide a separate support cradle, lowered/open front frame, removable service access and load design. An ordinary false-front sink base does not fit unchanged.

**Cabinet not supplied.** A nominal 36-inch base is only a planning minimum. Require at least 832.8mm clear width, the full flange and sloping bowl volume below the top, and separate faucet stem/nut/hose space. The manifest records exact keep-outs. Keep drawers, shelves and upper rails out of these volumes. The suggested cabinet origin is Y=45mm relative to the bowl; this requires a coordinated sink-specific frame.

Reserve 800mm in front for standing, with separate circulation as required. Trap, disposal, connectors, water services, waterproofing and sound support are not included. Sink/counter/faucet heat, wet, chemical and food-contact performance remain unverified pending selected products and installation details.

The Blender source, manifest and fresh-open receipt are alongside this README. All geometry and procedural finishes are original Homes project work or explicitly derived from the repository versions listed in the manifest. CC BY 4.0; attribute Homes project contributors. No manufacturer CAD or restricted source imagery is included.

Reproduce from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --asset white-apron-front-sink-32in
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --verify --render --asset white-apron-front-sink-32in
```

The generator preserves existing native files. Use a new version after adoption; never overwrite pinned assets. Verification reopens, resolves relative dependencies, checks native dimensions and open bowl/drain geometry, then produces the actual CPU preview. Render inspection passes for the visible function and openings, while home integration remains unchecked.
