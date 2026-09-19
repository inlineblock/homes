---
name: create-home
description: Develop and build a new home concept or a substantial architectural revision in this repository, starting with design exploration and a recorded design intent before modeling. Use as the entry workflow for creating or adding a home; keep isolated camera, material or cosmetic edits scoped to the requested change.
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
| Starting a new project | [templates/home](../../../templates/home/); adapt into `homes/<slug>/`, preserving the required organization rather than assuming existing project records |

## Explore before modeling

For a new home or substantial revision, compare a small number of genuinely distinct directions—normally two or three—within the user's constraints. Differences should affect space, use or architectural character, not merely color. When the user has already selected the form, explore the unresolved decisions within it.

Select the questions that matter to this house:

- How do massing, roof form, climate response, grade and structural rhythm work together?
- What makes arrival welcoming, parking practical and circulation direct? Where do privacy, storage and furniture operation constrain the plan?
- Which openings frame worthwhile views and daylight while respecting enclosure, room use, support and service needs?
- How do exterior materials and proportions continue into the entry, ceilings, beams, joinery or hearth? Carry timber, brick or another material indoors selectively when it strengthens the concept; do not spread a finish everywhere by default.
- Which signature space deserves emphasis, and which supporting spaces or systems make it believable? Consider outdoor use, furniture, lighting, appliances, drainage and maintenance alongside the hero view.

Critique each direction concretely. Identify anything flat, cheap-looking, uninviting or impractical through observable causes: weak proportions, repetitive textures, oversized blank surfaces, narrow arrival, unsupported spans, obstructed furniture or missing services. Explain a better design response, not simply a more expensive finish. Offer tailored improvements the brief suggests without adding unrelated luxury features.

Synthesize the strongest coherent direction. Record the recommendation, meaningful tradeoffs and any rejected alternative in **`homes/<slug>/design-intent.md` before generating the new or substantially revised building geometry**. Keep this concise: requirements/assumptions, options and critique, selected spatial/material moves, priority asset reuse/contributions, unresolved dependencies and views/checks that will test the intent. This is an observable design rationale, not a transcript of private reasoning or a ceremonial essay. Proceed within the authorized scope; this record is not an approval gate.

## Build, test the intent and refine

Use [home-asset-contribution](../home-asset-contribution/SKILL.md) to reuse suitable pins, publish missing repeated components or reviewed variations, and record actual adoption. Keep functional decisions in `program.md`; keep design rationale in `design-intent.md` and verification in `design-review.md`.

Apply [home-model-output-qa](../home-model-output-qa/SKILL.md) to the native model, plans and current outputs. Pair the exterior hero with corresponding interior views from the same scene: does the material language, spatial character and quality survive both? Inspect human-scale arrival and signature features as well as the flattering camera. Correct the underlying design when a view exposes a weak result; lighting or rendering polish cannot substitute for usable geometry. Preserve the agreed brief, update affected records, and report remaining limitations honestly.
