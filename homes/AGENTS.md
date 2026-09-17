# Home projects

- One home per folder. Begin with `project.json` and README; use `templates/home` for a new project.
- Keep editable sources in `model/`, presentation deliverables in `outputs/`, reference notes in `references/`, and unique assets in `assets/`.
- Store reusable content in the library and pin its version in `project.json`. Use relative links so a clone on another computer works.
- A layout change must update both the model and its outputs/plans/area schedule. Explain whether area includes walls, atria, porches, or garages.
- Keep rooms accessible, model door/window openings, and check circulation and furniture clearances. Do not count furniture placement as a resolved architectural layout.
- Preserve approved versions through Git; make reviewed changes on branches when collaboration is active. Coordinate edits to binary files.

## Required output organization
- Every home must have `outputs/README.md` as its visual index, `outputs/images/` for selected model renders, and `outputs/plans/` for PDFs, presentation boards, vector plans, and their PNG previews.
- Keep only the current reviewed result for each view or document. Regenerate into the same descriptive filename; do not create dates, `v001`, `history/`, `archive/`, `final-final`, or duplicate “latest” folders for outputs. Numeric view prefixes indicate different views, not revisions. Git retains previous revisions.
- Put experiments and unreviewed iterations in ignored `outputs/work/` or outside the repo. Visually inspect results before promoting them to the published output paths; a successful command alone does not make an image reviewed.
- Each home README must embed its primary image and link to its outputs index. The root README must show a labeled preview and outputs link for every home so collaborators can choose visually.
- Keep `project.json` deliverable paths, authoring tools, saved Blender render destinations, and all documentation aligned with this structure. Never leave a second copy in legacy `renders/` or `drawings/` folders.
- Editable models stay in `model/`. Shared library asset versions remain a separate dependency convention; do not add version folders to home outputs.
- Original designs, models, and outputs use CC BY 4.0; authoring code uses MIT. Preserve attribution and reference exclusions in `LICENSE.md`.
