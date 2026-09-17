# Atrium 01 generation

- `design.py` is the measured layout source. `build.py` assembles the native scene; drawing/export tools read the same layout.
- Keep kitchen-specific modeling in its own module and reusable primitives in `tools/common/`.
- Save models before rendering. Retain named cameras and a roof collection for review.
- Do not infer safety or engineering validity from a successful export. Report conceptual limitations in the README.
