# Coastal House authoring

- `design.py` owns dimensions, room boundaries, opening systems and deliverable view names. Keep measurements synchronized with the model, drawings and checks.
- `materials.py` publishes original reusable shaders; `furniture.py` owns detailed furnishings/joinery; `openings.py` owns moving panel geometry; `build.py` assembles architecture and environment.
- `render.py` writes drafts, never saves transient camera or closed-envelope states over the native model. `COASTAL_SAMPLES` and `COASTAL_PERCENT` are draft-only overrides.
- Verify the reopened file, relative assets, measured area, walking routes and panel clearance across the motion range. Report geometric checks separately from engineering or product approval.
- Rebuilds overwrite the generated native file. Inspect Git status and preserve any manual user model edits first. Published library versions are immutable.
