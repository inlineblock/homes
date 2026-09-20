# Botanical asset authoring

Seven deterministic family builders produce the **35 new families and 105 named variants** in the [landscape library](../../../library/landscape/README.md). The [visual gallery](../../../library/landscape/gallery.md) exposes actual whole-family and detail renders; the [catalog](../../../library/landscape/catalog.json) indexes exact native files, collections, dimensions and selection metadata. The six legacy plant families remain in their original folders and are not rebuilt by these tools.

All meshes and procedural materials are original. Asset geometry is CC BY 4.0 with attribution to Homes project contributors; code is MIT. Botanical sources inform shape and selection, but their photographs are not bundled or used as textures. These are architectural plant interpretations, not nursery products or certified taxonomic specimens.

## File ownership and running Blender

| Builder | Families | Variants |
|---|---|---|
| [mountain.py](mountain.py) | Aspen, Rocky Mountain maple, serviceberry, dogwood, kinnikinnick | 15 |
| [desert.py](desert.py) | Palo verde, desert willow, ocotillo, agave, barrel cactus | 15 |
| [xeric.py](xeric.py) | Blue grama, little bluestem, penstemon, fernbush, coneflower | 15 |
| [coastal.py](coastal.py) | Shore pine, silktassel, beach strawberry, sea oats, yaupon | 15 |
| [suburban.py](suburban.py) | Redbud, hydrangea, ninebark, hornbeam, laceleaf maple | 15 |
| [citrus.py](citrus.py) | Lemon, lime, orange, satsuma, grapefruit, kumquat | 18 |
| [orchard.py](orchard.py) | Avocado, fig, pomegranate, apple | 12 |

Separate Blender background processes can build different families at the same time. Assign exclusive output files to each agent, keep build processes to two CPU threads, and serialize GPU preview jobs. Several processes do not require several Blender installations. Do not let an asset build and its final preview/receipt race; finish geometry first, then verify and render that exact file.

Run from the repository root, with `blender` resolving to the installed binary:

```sh
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/library/plants/mountain.py
```

Use the corresponding builder in the table for another group. The exact family generator is also recorded in each `asset.json`. Some builders accept selected slug arguments after `--`; inspect that builder's entry point before selecting a subset. `--python-exit-code 1` is important because Blender otherwise may return success despite a Python exception.

The shared saver permits rebuilding an **untracked candidate** during review. Once any contents of a version are tracked, it refuses overwrite. Preserve committed/adopted versions and publish a new version or a distinct sibling; do not remove a tracked folder to bypass this rule. Rebuilding a candidate invalidates its previews, hashes and placement receipts.

## Shared geometry API

[common.py](common.py) batches many botanical pieces into a few meshes. Each family adds its own actual leaf, flower, fruit, spine or seedhead topology where the shared primitives are insufficient.

- `reset()` starts a clean authoring scene in meters, Z up. Never call it on an unsaved user scene.
- `collection(name)` creates one linked, persistent variant collection.
- `material(name, color, roughness=0.6, subsurface=0.0)` and `bark_material(name, color)` produce original procedural shaders. Colors are linear RGB or RGBA.
- `MeshBuilder(name, material)` batches `tube(points, radii, sides=7)`, `leaf(center, direction, length, width, style='oval', roll=0)` and `ellipsoid(center, scale, segments=10, rings=6)`, then `finish(collection)` writes the mesh.
- A leaf's center is its **blade center**. To attach its base to a twig, use `twig + normalized(direction) * length / 2`. `roll` is in radians. Shared styles are oval, lance, heart, lobed, needle and fan; custom leaf topology is appropriate for more specific morphology.
- Tubes need one radius per path point or one constant radius. Ellipsoids are for actual fruit/flower bodies; do not make spherical crowns and relabel them as trees. Finish only nonempty builders.
- `bounds(collection)` measures native mesh vertices and returns `min`, `max` and `dimensions` in meters.
- `save_family(slug, name, variants, metadata)` takes `(variant_id, collection, description)` tuples, saves a compressed native file, writes measured metadata and a collection-use README. Supply exact generator/command, botanical identity, source links, cultivar/training/rootstock intent where applicable, site limitations and original rights.

Collections intentionally share the same planting origin in the family file. Link the one named variant needed for a planting instance, rather than adding every overlapping collection to a home. Use recorded modeled dimensions; uniform scale 0.9–1.1 and Z rotation provide modest composition variation. Different growth habits require different geometry.

## Verification and native previews

1. Finish the geometry and save the family. Confirm stems, petals, leaf bases and fruit attachment, ground contact, coherent seasonal state and plausible scale.
2. Run [verify.py](verify.py) in a **fresh process**. It reopens each native file, checks all three measured variant bounds and geometry/materials, then links the real collections into an empty test host and verifies evaluated instances.
3. Run [preview.py](preview.py) after the native source stops changing. It renders all three variants and a close detail from the actual model; final review must inspect both images. Improve the source when topology, attachment, silhouette, shading or detail is weak, then repeat the dependent checks.
4. Build and independently reopen the [comparative nursery](../../../library/landscape/nursery/README.md). Its six separated beds test actual relative links, planting origin, spacing and path clearance. Do not present this as a proposed cross-climate garden or a real home's adoption.
5. After actually inspecting the **current whole-family and detail images**, use [record_review.py](record_review.py) to record the reviewer and concrete findings. This explicit action records image hashes and promotes the scoped native review fields; it never detects or infers a visual pass itself. It rejects stale native verification or previews. Keep manifest, preview and validation source hashes current; a successful script does not imply visually acceptable geometry.

Example commands, from the repository root:

```sh
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/library/plants/verify.py -- --assets quaking-aspen
blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/library/plants/preview.py -- --assets quaking-aspen --samples 64
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/library/plants/nursery.py
blender -b --factory-startup -t 2 --python-exit-code 1 --python tools/library/plants/nursery.py -- --verify
blender -b --factory-startup -t 4 --python-exit-code 1 --python tools/library/plants/nursery.py -- --render
```

Check `preview.py --help` through Blender for its current options; GPU renders must use the coordinated queue. The nursery renderer reopens the saved scene, renders its overview and six group cameras at 2400 × 1500 with Metal and 64 maximum samples, then adds only existing images to its README. It does not rewrite the native scene. Use `--cameras overview desert` to rerender a subset and `--samples` to change the sample ceiling. Native previews are not Image Gen studies. Image Gen belongs after a home's native geometry and composition review and must preserve actual plant detail.

`record_review.py` runs with ordinary Python and requires `--assets`, `--reviewer` and `--notes`. Supply the actual reviewer and observed findings after inspection. Never call it automatically after rendering or use generic placeholder approval text. Its pass is scoped to architectural concept landscaping, not photographic macro vegetation, horticultural certification or existing-home adoption.

## Adoption and status

**Modeled → reopened and visually reviewed → placement demonstrated → deliberately adopted in a home.** Keep these states distinct. The nursery establishes a controlled placement test; the target home still needs terrain contact, circulation and sightline checks, region/climate selection, root-zone/irrigation assumptions and a reviewed composition. Update the home's exact asset pins and schedule only after linking its chosen variants.

Follow the [canonical asset workflow](../../../docs/assets.md) and [landscape guidance](../../../library/landscape/AGENTS.md). New source revisions must update their dependent previews and nursery hashes before publication; preserve version history through Git and explicit asset versions, not duplicate dated output folders.
