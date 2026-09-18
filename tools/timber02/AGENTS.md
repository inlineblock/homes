# Timber Courtyard tools

- Exterior composition is authoritative; the image's room layout is not. Keep exact area inputs in `design.py`.
- Reuse the shared geometry, material, landscape, and library tools. Pin shared `.blend` assets by version and use relative links.
- Author standing seams as geometry and timber at real board scale; avoid fake image overlays as a substitute for the model.
- Render a front exterior and elevated view, then inspect both before reporting completion. Keep schematic interiors explicitly labeled.
- `gallery.py` owns camera names/poses and stable render filenames. For a camera-only gallery extension, use `prepare_gallery.py` on the saved native model; it checks that non-camera geometry, effective materials, lights and visibility remain unchanged.
- `verify_gallery.py` is the fresh-file validation entry point without rendering. `render_gallery.py` writes candidates only to ignored `outputs/work/`; inspect pixels before promotion and never save temporary cutaway states over the native scene.
