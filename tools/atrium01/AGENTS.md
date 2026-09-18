# Atrium 01 generation

- `design.py` is the measured layout source. `build.py` assembles the native scene; drawing/export tools read the same layout.
- Keep kitchen-specific modeling in its own module and reusable primitives in `tools/common/`.
- Save models before rendering. Retain named cameras and a roof collection for review.
- Do not infer safety or engineering validity from a successful export. Report conceptual limitations in the README.
- Camera-only gallery work uses `gallery_cameras.py` on the saved native file, then fresh `--verify-gallery` reopening; preserve approved geometry and record its fingerprint. Keep camera definitions in `design.py` for future builds.
- `render_views.py` writes named drafts into ignored `outputs/work/`. Inspect before promoting stable filenames. Both home and output READMEs embed the reviewed front/rear/side, interior, atrium-feature and single-level plan views.
