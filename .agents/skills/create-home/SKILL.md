---
name: create-home
description: Develop and build a new home concept or a substantial architectural revision in this repository, starting with design exploration and a recorded design intent before modeling, and finishing with the matching Sites portfolio update. Use as the entry workflow for creating or adding a home; keep isolated camera, material or cosmetic edits scoped to the requested change.
---

# Create a home

Turn the brief into a considered architectural direction before producing geometry. Proactively expand useful ideas within the brief; do not wait for the user to request every design consideration. This workflow coordinates the existing skills rather than replacing the design handbook.

## Understand the actual assignment

Read root/home guidance and the existing brief, program, review and source references when present. For a new home, establish these records from the brief and repository conventions as work proceeds. Inspect actual prior renders and plans when revising a home or using another project as context. Separate confirmed requirements, source observations, proposed changes and assumptions. Preserve explicit choices; identify unresolved constraints rather than inventing site, budget or engineering facts.

Use [home-program-review](../home-program-review/SKILL.md) to map the household, spaces, tier, climate/site, parking, storage, equipment and daily routes. Read relevant chapters through [the handbook index](../../../docs/design-guide/README.md), plus [the shared catalog](../../../library/README.md). Inspect candidate manifests rather than treating an asset's name as proof of fit. Cosmetic work should revisit only affected design decisions, not trigger a whole-home redesign.

## Repository navigation

All paths in this map are relative to the repository root; read scoped files **when present**.

| Purpose | Where to look |
|---|---|
| Repository rules and project catalog | [AGENTS.md](../../../AGENTS.md), [README.md](../../../README.md) |
| Home requirements and decisions | [homes/AGENTS.md](../../../homes/AGENTS.md), then `homes/<slug>/AGENTS.md`, `brief.md`, `project.json`, `program.md`, `design-intent.md`, `design-review.md` and `references/README.md` |
| Design requirements and choices | [Program checklist](../../../docs/home-program-checklist.md), [home standard](../../../docs/home-design-standard.md) and the relevant handbook chapters |
| Authoring and delivery instructions | `tools/AGENTS.md`, `tools/<authoring>/AGENTS.md`, plus the target home's scoped `model/AGENTS.md`, `outputs/AGENTS.md` and `outputs/images/AGENTS.md` |
| Shared artifacts and exact versions | [library/AGENTS.md](../../../library/AGENTS.md), catalog and applicable category/family/version `AGENTS.md`; `library/<category>/<asset>/<version>/asset.json` supplies dimensions, origins, rights and dependencies |
| Actual home artifacts | Native/deliverable paths in `project.json`; `assets/README.md` for adoption; `gallery.json`, `outputs/README.md`, `outputs/images/` and `outputs/plans/` for current visuals |
| Website delivery | [Sites directory](../../../sites/README.md), [collection instructions](../../../sites/home-collection/README.md), and `sites/home-collection/.openai/hosting.json` |
| Starting a new project | [templates/home](../../../templates/home/); adapt into `homes/<slug>/`, preserving the required organization rather than assuming existing project records |

## Explore before modeling

For a new home or substantial revision, compare a small number of genuinely distinct directions—normally two or three—within the user's constraints. Differences should affect space, use or architectural character, not merely color. When the user has already selected the form, explore the unresolved decisions within it.

Select the questions that matter to this house:

- How do massing, roof form, climate response, grade and structural rhythm work together?
- What makes arrival welcoming, parking practical and circulation direct? Where do privacy, storage and furniture operation constrain the plan?
- Which openings frame worthwhile views and daylight while respecting enclosure, room use, support and service needs?
- What clear ceiling heights suit each room and floor, the intended character and the room proportions? Choose and record them explicitly before modeling; do not inherit a default wall height. Distinguish finished-floor-to-finished-ceiling height from floor-to-floor height. Allow for floor/roof structure, ducts, beams, soffits, slats and lighting, including local reductions. Coordinate stairs, glazing and door heads with those decisions. Taller ceilings are a design choice, not a universal requirement for expensive homes.
- How do roof silhouette, window composition, recesses and shaded outdoor spaces give the house character from front, back and side? Avoid solving every elevation with generic roofs or arbitrary vertical material stripes.
- How do exterior materials and proportions continue into the entry, ceilings, beams, joinery or hearth? Carry timber, brick or another material indoors selectively when it strengthens the concept; do not spread a finish everywhere by default.
- Which signature space deserves emphasis, and which supporting spaces or systems make it believable? Consider outdoor use, furniture, lighting, appliances, drainage and maintenance alongside the hero view.

When a user supplies a reference, identify exactly what they value—exterior silhouette, material tones, window composition or spatial idea—and what may change. Do not copy the reference floor plan by default when the request is exterior-only. Record this distinction in the design intent.

Review a coordinated palette at both facade and close-up scale: neutral temperature, the proportion of contrasting finishes, transitions at architectural boundaries, texture scale, grain direction, mortar and bond, roughness, finish variation and how daylight shifts the colors. Check the palette under neutral daylight before relying on dramatic hero lighting. Do not rely on flat color blocks or harsh white/black contrast to signal quality. Preserve explicit palette choices without making one home's driftwood, brick or roof treatment universal.

Critique each direction concretely. Identify anything flat, cheap-looking, uninviting or impractical through observable causes: weak proportions, repetitive textures, oversized blank surfaces, narrow arrival, unsupported spans, obstructed furniture or missing services. Explain a better design response, not simply a more expensive finish. Offer tailored improvements the brief suggests without adding unrelated luxury features.

Synthesize the strongest coherent direction. Record the recommendation, meaningful tradeoffs and any rejected alternative in **`homes/<slug>/design-intent.md` before generating the new or substantially revised building geometry**. Keep this concise: requirements/assumptions, options and critique, selected spatial/material moves, priority asset reuse/contributions, unresolved dependencies and views/checks that will test the intent. This is an observable design rationale, not a transcript of private reasoning or a ceremonial essay. Proceed within the authorized scope; this record is not an approval gate.

## Coordinate independent critique

For a broad new home or substantial architectural revision, delegate bounded reviews of architecture/materials, program/circulation and site/climate as appropriate. Give each agent clear ownership and reference the actual brief, views and shared catalog. Synthesize the findings into one coherent direction rather than assembling unrelated suggestions. Before final promotion, have an independent reviewer inspect actual exterior/interior renders for design and visual defects; Fix functional failures, geometry errors and material/render defects before promoting affected outputs. Only genuinely unresolved site, product or engineering decisions may remain documented as limitations; recording a fixable defect is not review closure. Assign one owner per native binary and coordinate heavy rendering. For repeated workflow gaps, improve the existing skill; delegate a new skill draft and independent trial only when no existing skill covers the work.

## Build, test the intent and refine

Use [home-asset-contribution](../home-asset-contribution/SKILL.md) to reuse suitable pins, publish missing repeated components or reviewed variations, and record actual adoption. Keep functional decisions in `program.md`; keep design rationale in `design-intent.md` and verification in `design-review.md`. Record selected clear heights by room or room group and floor, floor-to-floor datums, assembly/service allowances and any local exceptions. Explain how the choices support the brief and room proportions.

Apply [home-model-output-qa](../home-model-output-qa/SKILL.md) to the native model, plans and current outputs. Pair the exterior hero with corresponding interior views from the same scene: does the material language, spatial character and quality survive both? Inspect human-scale arrival and signature features as well as the flattering camera. Verify modeled clear heights to the lowest relevant fixed ceiling element, including beams and soffits, and inspect interior views from a normal human eye height with correctly scaled furniture. Check that the intended ceiling proportions survive the actual structure, lighting and finishes; do not use stretched furnishings or camera distortion to imply height. Correct the underlying design when a view exposes a weak result; lighting or rendering polish cannot substitute for usable geometry. Preserve the agreed brief, update affected records, and report remaining limitations honestly.

## Finish with Image Gen

After the native model and its render gallery pass visual review, complete the [Image Gen photographic pass](../home-model-output-qa/SKILL.md#image-gen-after-native-render-review). This is a required finishing step for a completed home: use the reviewed exterior render as the image-edit reference, preserve its design and camera, inspect the generated result, and lead the home page with the selected photographic study. Plan a generous photographic tour by default, including multiple exteriors, kitchen/living interiors and signature features from their corresponding reviewed renders; do not wait for separate requests for each image. The minimum gallery is a floor, not a target or cap. Keep the native gallery and plans alongside them. Do not stop at Blender renders or use Image Gen to conceal unresolved architecture.


## Update the home website

A new home or substantial revision is not fully delivered until its collection entry and individual page in `sites/home-collection/` reflect the reviewed result. This website update is part of the user's standing home-delivery convention. Keep all website work under `sites/`, preserve the established luxury design system, and retain the architectural sources under `homes/`. For a narrow visual change, refresh only the affected website content; do not trigger unrelated redesign work.

1. **Reuse the existing Site.** Read the [collection instructions](../../../sites/home-collection/README.md) and apply the installed `sites-building` and `sites-hosting` skills. Reuse the exact `project_id` in `.openai/hosting.json`; do not create a replacement Site or one Site per home. Preserve its current audience, initially private. The Site owner handles source changes and publishing; architectural subagents return their artifacts without independently editing or publishing the Site.
2. **Bring the source records current first.** Use the home's `project.json`, `gallery.json`, reviewed photographic studies, native renders and all occupied-level plans. Include available PDF/SVG downloads. Preserve area conventions, image provenance and concept labels; remove obsolete status notes only when review evidence resolves them. Do not publish experiments, private reference material or identifying property details. If the home is still in development, label the page accordingly and show only approved material; do not imply that its model or plans are complete.
3. **Update page content and membership.** Edit `src/features/residence/editorial.json` for the home's description and status. For a new home, add its slug to `scripts/generate.py`'s current explicit `order` list and supply its editorial record. Inspect that generator's home-specific area/status rules and incomplete-gallery fallback: the current fallback assumes Twin Gables reference filenames and must not be reused blindly. Update collection totals, navigation, metadata, validation expectations and documentation when membership changes. Current fixed counts appear in `src/design-system/components.py`, both feature `page.py` files, and `scripts/render.py` / `scripts/validate.py`; prefer deriving counts from the collection when changing these.
4. **Refresh the exported site.** From `sites/home-collection/`, run `python3 scripts/generate.py`. This refreshes HTML, optimized images, plan downloads, `src/content-snapshot.json` and `src/asset-sources.json`. `scripts/render.py` only renders the existing snapshot; it does not import revised home content. Inspect the changes for stale images/downloads and unintended updates to other homes, especially when other work is active. Keep generated output and source together.
5. **Check the result.** Run `python3 scripts/validate.py` and `node --check src/design-system/site.js`. Visually inspect the collection entry and affected home page at desktop and mobile sizes; exercise gallery viewing, floor-plan links and next-home navigation. Confirm the page uses the reviewed revision and every available occupied-level plan. Resolve broken links, missing images and misleading status or area claims before publication.
6. **Publish and report.** Follow the installed Sites hosting workflow from the nested Site repository, without committing or pushing the parent architectural repository to the Sites remote. Publish to the existing Site unless the user explicitly requests local-only work or no publishing. Confirm terminal deployment success and return the live URL. If publication is blocked, retain the finished local update and distinguish it from the still-live version; do not report the website as updated online.
