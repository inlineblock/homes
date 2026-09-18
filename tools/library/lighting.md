# Shared lighting

Use quiet recessed ceiling fixtures for general illumination, concealed under-cabinet bars for work surfaces, and a deliberate pendant at a focal table or island. The existing `fixtures/opal-globe-pendant/v001` remains the rounded showpiece alternative to the new linear pendant. A room still needs a considered layout and useful task light; adding a glowing mesh does not establish adequate lighting.

| API key | Shared collection, v001 | Mounting and size |
| --- | --- | --- |
| `downlight` | `fixtures/lighting-recessed-downlight-3in` | Ceiling plane at Z=0; 3-inch light aperture, 3.6-inch outside trim, 3.336-inch housing diameter |
| `taskbar` | `fixtures/lighting-undercabinet-bar-4ft` | Top mounting plane at Z=0; 48 inches along X; emits down |
| `linear` | `fixtures/lighting-linear-pendant-4ft` | Canopy top at Z=0; 48 inches along X; bottom 31.848 inches below ceiling |

The downlight requires a **3.4-inch ceiling cutout and 3.6 inches of clear service depth above the ceiling**. Model the opening and check the roof/ceiling buildup. Its housing cannot be placed through a solid slab. The generic asset has no fire, insulation-contact, wet-location, or coastal-corrosion rating; actual product selection remains open.

```python
from common.lighting_assets import load, place, dependencies
lighting = load(ROOT, keys=['downlight', 'taskbar'])
# Placement coordinates are feet, rotations are radians about Z.
place('Kitchen downlight', lighting['downlight'], 'downlight', (12, 16, 10), power=8)
place('Kitchen concealed task bar', lighting['taskbar'], 'taskbar', (12, 20, 4.5), power=12)
pins = dependencies(keys=['downlight', 'taskbar'])
```

The immutable linked collection contains the manufactured geometry and low-emission diffuser. `place` adds a separate parented, host-owned area light. Its power can be edited per instance; set `power=0` for geometry only. Watt settings are illustrative Blender illumination, not a lumens calculation or tested product photometry. Do not use heavy diffuser emission as a substitute for controlled light sources. All library paths must become repository-relative before saving the adopting home.

Publish only missing versions and verify in a separate Blender process:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --factory-startup --background --python-exit-code 1 --python tools/library/publish_lighting.py
/Applications/Blender.app/Contents/MacOS/Blender --factory-startup --background --python-exit-code 1 --python tools/library/publish_lighting.py -- --verify
```

The verifier loads the saved collections, checks measured bounds and external image dependencies, and renders real 800-pixel CPU Cycles previews. Inspect those previews before adopting the assets. Its current receipt is `lighting-validation.json`. Original meshes and shaders are CC BY 4.0 with attribution to Homes project contributors; source code is MIT. These are generic original concept assets, not commercial fixture models.
