# Mountain authoring

- design.py owns dimensions and area/storey conventions. build.py assembles envelope/structure, interior.py owns room placement, site_model.py owns terrain/arrival, draw_plans.py reads the same dimensions.
- Generic finishes/furnishing primitives live in common/; new repeated components must be library collections, not copied functions in this home.
- Keep deterministic forest placement, clear camera corridors, and all plant origins on evaluated grade.
- Never regenerate over unpreserved manual model edits. Render review files into ignored outputs/work; final promotion follows actual inspection.
