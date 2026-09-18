# Hardware collection

Original reusable details for cabinet fronts, doors and pocket sliders. Five families are available in **satin bronze**, **matte black** and **brushed steel**. These are generic concept components, not commercial product specifications.

| Family | Nominal dimensions | Mounting |
|---|---|---|
| Round knob | 1⅛ in diameter, 1.10 in projection | Face center; single fixing |
| Slender bar pull | 6 in centers, 6.4 in width, 1¼ in projection | Horizontal by default; rotate about local Y for vertical |
| Edge pull | 4 in width, 1⅛ in projection | Top/front edge; recess .12 in top return |
| Door lever | 2 in rose; 5 in lever reach | Spindle center; one face; host supplies latch/opposite lever |
| Flush sliding-door pull | 1¾ × 5 in face, .55 in recess | Cut a 1.45 × 4.70 in host pocket, at least .65 in deep |

All collections use meters internally, Z-up, front toward **-Y**, and the mounting face as origin. Keep scale at 1. Finish selection is explicit in the asset slug, so a home's dependencies reproduce the same appearance. Each folder contains a native collection, manifest and actual rendered preview.

Authoring API: `common.hardware_assets.place(root, kind, finish, name, loc_ft, rotation_z=0)`. The placement coordinates are feet to match the home generators. Use `dependencies([(kind, finish), ...])` to record the exact assets in a home's manifest. For a vertical pull, rotate the returned instance around its local Y axis by 90 degrees.

Publish missing versions with `tools/library/publish_hardware.py`; validate and render with `Blender --factory-startup --background --python tools/library/verify_hardware.py -- --render` (no BIM add-ons are required for these standalone collections). The generator never overwrites an existing version.

## Actual asset previews

| Family | Satin bronze | Matte black | Brushed steel |
|---|---|---|---|
| Round knob | ![Round knob — satin-bronze](round-knob-satin-bronze/v001/preview.png) | ![Round knob — matte-black](round-knob-matte-black/v001/preview.png) | ![Round knob — brushed-steel](round-knob-brushed-steel/v001/preview.png) |
| Bar pull | ![Bar pull — satin-bronze](bar-pull-satin-bronze/v001/preview.png) | ![Bar pull — matte-black](bar-pull-matte-black/v001/preview.png) | ![Bar pull — brushed-steel](bar-pull-brushed-steel/v001/preview.png) |
| Edge pull | ![Edge pull — satin-bronze](edge-pull-satin-bronze/v001/preview.png) | ![Edge pull — matte-black](edge-pull-matte-black/v001/preview.png) | ![Edge pull — brushed-steel](edge-pull-brushed-steel/v001/preview.png) |
| Door lever | ![Door lever — satin-bronze](door-lever-satin-bronze/v001/preview.png) | ![Door lever — matte-black](door-lever-matte-black/v001/preview.png) | ![Door lever — brushed-steel](door-lever-brushed-steel/v001/preview.png) |
| Flush pull | ![Flush pull — satin-bronze](flush-pull-satin-bronze/v001/preview.png) | ![Flush pull — matte-black](flush-pull-matte-black/v001/preview.png) | ![Flush pull — brushed-steel](flush-pull-brushed-steel/v001/preview.png) |
