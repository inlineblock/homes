# Authoring tools

- Keep shared geometry/material helpers separate from per-home layout data and scene assembly. Avoid a giant script that intermixes every home.
- Use deterministic seeds, repository-relative paths, and explicit units. Geometry, plan drawings, and area schedules should derive from the same project inputs.
- Support regeneration without deleting user-authored models: save or commit edits first, and document which outputs the generator overwrites.
- Keep dependencies small and use Blender's bundled Python for Blender work. Record exact tested Blender/Bonsai versions.
- Verification should check useful invariants: area, room counts, asset links, saved-file reopening, and rendered appearance. Avoid tests that simply restate the implementation.
- Write current deliverables to the home's `outputs/images/` and `outputs/plans/`, using stable filenames. Follow `homes/AGENTS.md` for output review, galleries, and history policy. Keep saved Blender render paths relative to the model.
