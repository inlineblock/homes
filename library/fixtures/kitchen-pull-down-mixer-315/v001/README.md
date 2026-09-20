# Shared pull-down kitchen mixer · v001

![Actual native installation study](preview.png)

Original, dimensioned concept geometry. The preview uses the published native asset in a real cutout study; the plain studio supports are not a cabinet supplied by this package. No home has adopted this version yet.

The original published mixer arch and lever were extracted from `fixtures/kitchen-sink-mixer-650/v002`, retaining its brushed stainless material. This adds a distinct docked pull-down head, integrated valve body, mounting stem and nut. The source version remains unchanged.

The origin is the mounting center at finished countertop top, Z=0. The spout faces −Y with 315mm reach; the outlet is 230mm above the top. Use a 35mm single deck bore, keep the 44mm nut envelope clear at Z=−60mm, and reserve 150mm below the counter for an unselected hose/weight arrangement. The modeled stem extends 75mm down. Allow 120mm to the right for the lever and 50mm behind the body. The 450mm pull-out reach is a concept allowance, not a rated or animated mechanism.

The head is shown docked. No hose, counterweight, internal valve, water performance or certified product installation is represented.

The Blender source, manifest and fresh-open receipt are alongside this README. All geometry and procedural finishes are original Homes project work or explicitly derived from the repository versions listed in the manifest. CC BY 4.0; attribute Homes project contributors. No manufacturer CAD or restricted source imagery is included.

Reproduce from the repository root:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --asset kitchen-pull-down-mixer-315
/Applications/Blender.app/Contents/MacOS/Blender -b --factory-startup --python tools/library/publish_kitchen_sink_options.py -- --verify --render --asset kitchen-pull-down-mixer-315
```

The generator preserves existing native files. Use a new version after adoption; never overwrite pinned assets. Verification reopens, resolves relative dependencies, checks native dimensions and open bowl/drain geometry, then produces the actual CPU preview. Render inspection passes for the visible function and openings, while home integration remains unchecked.
