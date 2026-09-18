# Coastal editable models

- Keep `coastal-house.blend` fully furnished, with complete roofs/walls and named cameras. Frame 1 closes both sliding systems; frame 120 moves panels into their pockets. Save the open state as the default.
- Do not put solid wall geometry through the moving panels or their pockets. Keep counter stone below the window tracks. Check intermediate animation positions, not only endpoints.
- Keep kitchen work aisles, bedroom entries, the entry spine and rear terrace route unobstructed. A rendered opening is not proof of access; inspect the reopened model's bounding geometry.
- `coastal-house.ifc` is classified architectural concept geometry, not a fully parametric construction model. Export the closed envelope at frame 1 without overwriting the Blender open-state file.
- Retain four relative library links and pin versions in project.json. Changes to shared materials require a new library version.
