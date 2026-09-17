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
- Save native sources, inspect actual rendered images, and confirm important files can reopen. A script that runs is not sufficient visual QA.
- Record software versions, relative paths, asset dependencies, and generation commands. Keep downloads and caches outside Git.
- Use Git LFS for binary models and selected media. Commit source and dependencies together; do not silently publish or choose a public remote.
- Do not introduce paid assets, subscriptions, or third-party content with incompatible redistribution terms. Record asset origins.
- Update the nearest guidance file when the user asks to establish a new lasting project convention. Keep guidance scoped and avoid duplicating entire parent files.
