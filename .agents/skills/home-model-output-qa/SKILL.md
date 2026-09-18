---
name: home-model-output-qa
description: Build, reopen, and visually review this repository’s Blender home models, IFC exports, render sets, and dimensioned concept plans before promoting current outputs. Use for new homes, coordinated home revisions or README gallery coverage audits, not generic image generation.
---

# Home model and output QA

Work from the repository root; paths below are repository-relative. Read applicable AGENTS.md, the home’s README, `project.json`, `program.md`, and `design-review.md`. Apply [design standards](../../../docs/home-design-standard.md), [program checklist](../../../docs/home-program-checklist.md), relevant [design-guide chapters](../../../docs/design-guide/README.md), and [asset adoption rules](../../../docs/assets.md); keep climate and tier decisions there rather than duplicating them here.

## Preserve and coordinate

Inspect Git status and native-file changes before regeneration. Preserve manual work; never overwrite an unpreserved edited model. Read the home’s authoring instructions to identify overwritten files and exact regeneration commands. Coordinate binary ownership and serialize heavy GPU rendering with other agents when needed. Discover installed Blender/Bonsai and document runtimes; record tested versions and commands without baking one machine’s paths into reusable tools. If the environment requires escalation for Blender, use its approval mechanism; this skill grants no additional commit, publication, or installation authorization.

For a gallery-only task, preserve approved geometry, materials, lights and layout. Inventory existing reviewed outputs first, add only missing camera views, and verify native reopening plus camera/source consistency. Do not force a whole-home redesign or regenerate unchanged IFC and drawings solely to add a README image. Record any design limitations revealed by the new angle.

## Validate the actual scene

Use the home’s dimensional source for geometry, drawings, and area schedules. Pin linked asset versions in `project.json` and `assets/README.md`; follow the library contribution workflow for missing repeated parts.

Reopen the saved native file in a fresh Blender process and run its home-specific verifier. Check measured floor areas and exclusions, storey datums, rooms, modeled bedroom storage, parked-car/pedestrian routes, welcoming arrival, furniture operation, and access to every room. Include appliance and cabinet door opening envelopes, stairs/landings/headroom/guards, moving glazing at intermediate states, and deck support/terrain contact where applicable. Test evaluated linked-instance geometry, not merely object names or empty instance bounds. A collision-free narrow corridor is not proof of a pleasant entry. Record unresolved checks honestly.

[Repository verification](../../../tools/common/verify_repository.py) checks native reopening, relative dependency paths, floor area, and bed counts; it does not prove the full design standard. Confirm LFS files are real models rather than pointer stubs and dependencies remain inside the checkout.

Export the intended envelope state through [IFC export](../../../tools/common/export_scene_ifc.py); inspect collection classification and storey mappings for this home. Reopen and schema-check the IFC, then use [Bonsai verification](../../../tools/common/verify_bonsai.py) in a separate process. Do not save temporary render/cutaway/export states over the canonical furnished model. Distinguish classified concept geometry from a complete semantic building model.

## Review before promotion

Generate drafts in ignored `outputs/work/`. Inspect actual front/arrival, rear/outdoor, side or elevated roof/site views, and relevant interiors. Check mutual consistency, roof drainage concept, ground contact, floating plants, obstructing foliage, believable furniture/material scale, hardware placement, glazing, light exposure, and camera composition. Compare opening states from identical cameras when demonstrating movement. Generated illustrations cannot stand in for native model renders.

Render PDF pages to images and inspect every page alongside its furnished plan: dimensions, labels, fixtures, openings, circulation, clipping, and embedded images must match the current scene. Fix defects and regenerate affected artifacts before promotion.

Promote only reviewed images and documents into stable `outputs/images/` and `outputs/plans/` filenames. Refresh dependent boards/previews, output index, home/root galleries, manifest, asset schedule, and design-review evidence together. Keep no output history/version folders; Git retains revisions. Report exactly which checks passed and which remain unresolved; neither rendering nor schema validation establishes engineering, code, or permit approval.

## Gallery completeness

Apply the [required visual gallery](../../../homes/AGENTS.md#required-visual-gallery), including distinct exterior/interior coverage, every occupied level and clearly pictured signature features. Inventory actual image contents rather than counting filenames or treating cutaways as exterior views. Update each home’s `gallery.json`, embed the selected set directly in its README and output index, and refresh the root catalog. Run [gallery verification](../../../tools/common/verify_galleries.py), then visually check the image/caption sequences and plans. Missing views require reviewed native renders; a passing file count is not visual approval.
