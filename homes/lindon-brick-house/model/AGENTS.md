# Lindon native sources

- One agent owns the Blender binary. Regenerate only after preserving manual edits and coordinating source changes.
- Read [authoring instructions](README.md). Keep `design.py`, proposed openings, furnishings, actual floor voids, drawings and receipts consistent.
- Use the adopted `Deep iron red brick | running bond | v003` shader. Preserve earlier versions for existing consumers. Apply `Brick meters` UVs after final transforms, including the angled garage wing.
- Stair floor openings and ceiling openings differ by level. Use `voids` for slabs and `ceiling_voids` for ceilings; a renderer must not seal the flight with a ceiling plane.
- Keep roof face normals upward before adding inward thickness; inspect both roof slopes so thickened faces cannot bury seams. Close garage roof strips outside the upper footprint without covering occupied floors.
- Read shared appliance origin metadata before mounting. Sink and cooktop bodies need real host apertures; inspect the exposed glass/basin in the native render.
- An imported IFC is classified concept geometry. Do not describe the source as an as-built, engineered model or complete permit package.
