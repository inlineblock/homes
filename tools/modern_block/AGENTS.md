# Modern Block authoring and reproduction

## Ownership and source boundaries

- Follow [parent tooling guidance](../AGENTS.md), the [home brief](../../homes/modern-block/brief.md) and [design intent](../../homes/modern-block/design-intent.md). Keep identifying reference names, people, locations, addresses, social links and source-property URLs out of every repository artifact and metadata field.
- `design.py` owns meter dimensions, room zones, stair/void geometry and area constants. `envelope.py` builds walls, actual openings, stone module placement, roofs and drainage intent. `interiors.py` places linked equipment/storage/furniture and writes measured plan records. `utils.py` provides metric adapters; shared `common.geometry` helpers use feet and must be converted explicitly.
- `build.py` owns full scene assembly, site, planting, screens, cameras, illumination and save. `facade_details.py` owns projecting entry/reveals and the external pier; `site_context.py` owns connected driveway and grouped garden-edge placement. `draw_plans.py` reads the same design constants, generated `interiors-layout.json` and `model/opening-schedule.json`. Never repair a coordinated layout only in a drawing. `schedule.py` owns the grouped adoption record and checks exact project/library pin equality.
- `kitchen_layout.py` owns the revised kitchen's module coordinates, counter height and island footprint. `kitchen.py` installs the versioned concealed-equipment kit and records its actual plan placements through `interiors.py`. Run `verify_kitchen.py` against the saved native model after changing equipment, mounting or operation space; the library's isolated preview does not establish host fit.
- Assign one agent/person as owner of `model/modern-block.blend` and generated IFC for a run. Other contributors own separate text modules. Serialize scene builds and coordinate GPU rendering; no competing writers to either binary or one draft image path.
- Inspect Git status and preserve manual model edits before rebuilding. Existing adopted library versions are immutable. Publish missing reusable geometry under `library/` and explicitly change adoption pins; do not make private repeated plant, equipment or furniture copies here.

## Environment and dependencies

- Tested native version: **Blender 4.5.14 LTS**. The repository software record identifies **Bonsai 0.8.5 / IfcOpenShell 0.8.5**; the current Bonsai receipt proves a fresh IFC import but does not independently encode its add-on version. Consult [software setup](../../docs/software.md) when reproducing on another installation.
- Run from repository root. Set `MODERN_BLOCK_BLENDER` to the installed Blender executable and `MODERN_BLOCK_PYTHON` to a Python environment with Matplotlib; otherwise the commands below use `blender` and `python3` from PATH. Do not hardcode a user's application path, extension directory or interpreter path into source.
- Blender uses its bundled Python for scene work. IFC export requires IfcOpenShell importable in that environment; Bonsai verification requires an enabled compatible Bonsai extension and a normal user startup. Build/geometry verification use `--factory-startup` to avoid unrelated add-on workspace links. Export/import processes do not save over the presentation model.
- Restore actual Git LFS objects before opening files. Keep all pinned `library/**/asset.json` and native dependencies together with source; relative linked material dependencies are part of the portable model. `project.json`, `assets/README.md` and the saved model must agree.

## Reproduce and review

Build the current native scene, then verify it in a separate process:

```sh
"${MODERN_BLOCK_BLENDER:-blender}" --background --factory-startup --python-exit-code 1 --python tools/modern_block/build.py
"${MODERN_BLOCK_BLENDER:-blender}" --background --factory-startup homes/modern-block/model/modern-block.blend --python-exit-code 1 --python tools/modern_block/verify.py
"${MODERN_BLOCK_BLENDER:-blender}" --background --factory-startup homes/modern-block/model/modern-block.blend --python-exit-code 1 --python tools/modern_block/verify_kitchen.py
"${MODERN_BLOCK_PYTHON:-python3}" tools/modern_block/schedule.py
```

The build overwrites `model/modern-block.blend`, `model/opening-schedule.json`, `project.json`, `assets/README.md` and `tools/modern_block/interiors-layout.json`. The schedule writer restores grouped family/use descriptions and rejects unclassified or stale pins; keep it invoked after the build's generated dependency list. Verification overwrites `model/native-validation.json`. Do not infer visual approval from either command succeeding.

Render drafts to ignored work, inspect the actual images, then render final-quality work for selected cameras:

```sh
"${MODERN_BLOCK_BLENDER:-blender}" --background --factory-startup homes/modern-block/model/modern-block.blend --python-exit-code 1 --python tools/modern_block/render.py -- --draft --views 01-front-arrival 05-kitchen
"${MODERN_BLOCK_BLENDER:-blender}" --background --factory-startup homes/modern-block/model/modern-block.blend --python-exit-code 1 --python tools/modern_block/render.py -- --samples 96
```

`--views` accepts the saved camera names; omission renders all cameras. `--draft` uses half resolution and 20 samples. Full work uses saved 1800 × 1200 resolution and selected sample count. The renderer attempts Metal and otherwise uses CPU; verify actual device availability on the target machine. It writes `outputs/work/<camera>.png`, switches five screen leaves between closed and 75° open states, and does not save those transient states into the native file. Review useful composition, materials, actual openings, room access and both screen states before copying selected images into stable `outputs/images/` names.

Kitchen cameras 14 and 15 use identical framing for closed/open appliance comparison. Camera 16 shows the island microwave and waste pullout open; camera 17 shows the pantry garage and storage open. These temporary states link the library's declared `blender.operating_collections.open` collections. The saved home remains in its closed presentation state, and no renderer mutates the published library assets.

Export classified IFC and import it through Bonsai in separate normal-startup processes:

```sh
"${MODERN_BLOCK_BLENDER:-blender}" --background homes/modern-block/model/modern-block.blend --python-exit-code 1 --python tools/common/export_scene_ifc.py
"${MODERN_BLOCK_BLENDER:-blender}" --background --python-exit-code 1 --python tools/common/verify_bonsai.py -- modern-block
```

These overwrite `model/modern-block.ifc`, `model/ifc-validation.json` and `model/bonsai-validation.json`. The exporter includes classified concept geometry and explicitly classified linked windows/cladding; it is not a full semantic furniture/services model. Keep schema validation and actual Bonsai import evidence separate from native presentation geometry and engineering approval.

Generate plan drafts, inspect both furnished levels, then promote:

```sh
"${MODERN_BLOCK_PYTHON:-python3}" tools/modern_block/draw_plans.py
"${MODERN_BLOCK_PYTHON:-python3}" tools/modern_block/draw_plans.py --promote
"${MODERN_BLOCK_PYTHON:-python3}" tools/common/verify_galleries.py
```

Plans default to `outputs/work/plans/ground-floor` and `upper-floor` in PNG/SVG/PDF; `--promote` writes those stable names under `outputs/plans/`. The plan script uses a temporary Matplotlib cache and does not need a user-specific runtime path. Regenerate after actual layout/opening changes. Check text legibility, true furniture footprints, thresholds, storage and routes in the rendered plans before promotion.

Finish current native gallery coverage and registered plans before photographic finishing. Follow the [home output QA skill](../../.agents/skills/home-model-output-qa/SKILL.md), preserve native source hashes/provenance for AI studies, and refresh affected studies after source changes. Gallery validation checks registration and embedding, not picture quality. Keep experiments under ignored work; stable current files and Git retain the approved history.

`write_gallery.py` rebuilds the three gallery indexes and provenance from reviewed stable images and `outputs/photo-prompts.json`. Copy only inspected selections into stable image paths before invoking it.
