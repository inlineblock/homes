# Repository guidance

## Purpose and structure
- This repository contains architectural concept projects, reusable assets, and reproducible authoring tools. Read the root README and the target home's brief before editing.
- Each home belongs in `homes/<slug>/`; reusable assets belong in versioned folders in `library/`. Follow the more specific AGENTS.md files below this directory.
- Keep design decisions and measurements in text alongside binary models. Product/view code, if added, should be separated by feature with reusable UI components in their own design-system folder.
- Inspect Git status before work. Preserve user edits and existing artifacts. Check committed state and deployment evidence before assuming anything is production.

## Accuracy and honesty
- Use meters internally and feet/inches in presentation drawings unless the project says otherwise. State the area convention and exclusions.
- Distinguish an editable visualization, a semantic building model, a dimensioned concept drawing, and permit/construction documentation. Never label one as another.
- Mark unverified conditions explicitly. Do not invent a site, survey, structural calculations, product specification, or code approval.

## Deliverable standard
- Before drawing a new home, read `docs/home-design-standard.md` and inventory the shared library. A beautiful exterior does not excuse missing storage, poor arrival, inaccessible rooms, or absent parking.
- Reuse is required, not optional: search `library/**/asset.json` before making materials, plants, paving, cabinetry, fixtures or furniture. Link the existing suitable version. If a repeated component is missing, publish it to the library and instantiate it in the home; a copied generator function alone is not a shared asset.
- Record an asset-use schedule and a completed design review in each home's text sources. Identify exact dependencies and any deliberately bespoke geometry. Do not describe a project as reviewed with open failures in those records.
- Save native sources, inspect actual rendered images, and confirm important files can reopen. A script that runs is not sufficient visual QA.
- Meet the [required visual gallery](homes/AGENTS.md#required-visual-gallery) in every home README and outputs index: at least three exterior angles, two interiors, every occupied level's plan and dedicated signature-feature views. Keep the root README a compact directory: exactly one reviewed realistic AI photo beside one main/ground floor-plan preview per home, with links to its complete landing page. Full galleries belong on home pages, not the root. Validate with `python3 tools/common/verify_galleries.py`.
- Record software versions, relative paths, asset dependencies, and generation commands. Keep downloads and caches outside Git.
- Use Git LFS for binary models and selected media. Commit source and dependencies together; do not silently publish or choose a public remote.
- Do not introduce paid assets, subscriptions, or third-party content with incompatible redistribution terms. Record asset origins.
- Update the nearest guidance file when the user asks to establish a new lasting project convention. Keep guidance scoped and avoid duplicating entire parent files.

## Comprehensive design decisions
- Read `docs/home-program-checklist.md` and relevant `docs/design-guide/` chapters; create `homes/<slug>/program.md` before treating a new or substantially revised home as resolved.
- Respect this user's premium defaults: complete kitchen equipment, wide panel-ready refrigeration, primary double vanity, separate shower and tub, enclosed toilet room, coordinated hardware and recessed/task lighting with deliberate focal fixtures. Record reasoned exceptions instead of silently omitting them.
- Apply baseline functionality to every tier; climate, site, household and maintenance needs override prestige assumptions. Do not claim premium homes universally exclude a material such as asphalt shingles.
- Prefer existing library options. When modification is needed, preserve the adopted version, record derivation, publish a reviewed reusable variation, then explicitly adopt it. Follow `docs/assets.md`.

## Reusable project skills
- Start new homes and substantial architectural revisions with `.agents/skills/create-home/`: explore and critique tailored directions, record a concise `design-intent.md` before modeling, then follow the existing program, asset and output-review skills. Keep cosmetic edits scoped.
- Home delivery includes refreshing its collection entry and individual page in `sites/home-collection/`; follow [Create a home — website delivery](.agents/skills/create-home/SKILL.md#update-the-home-website) for content, validation and existing-Site publication. Respect explicit local-only requests.
- Use `.agents/skills/home-program-review/` for briefs, completeness and coordinated layout reviews.
- Use `.agents/skills/home-asset-contribution/` for library selection, adaptation and contribution.
- Use `.agents/skills/home-model-output-qa/` for native/IFC/render/plan verification and current-output promotion.
- Skills are repository-local and complement the scoped guidance. They do not authorize unrelated publication or external actions. Improve them when an actual recurring workflow demonstrates a missing instruction; do not add one-off preferences as universal rules.

## Specialist agents and recurring work
- For a broad new-home or library expansion, delegate independent, bounded specialties such as program/layout review, climate/envelope research, systems coordination, asset families and visual QA. Give each agent explicit file ownership; one agent owns each native binary. Coordinate shared rendering resources.
- When a workflow repeats and is not covered by an existing skill, delegate a repository-local skill draft and an independent trial on a real example. Prefer improving an existing skill over creating overlapping ones. Validate the skill and its links, then route to it from this guidance; keep detailed design policy in the handbook.
