# Shared original components

`common.shared_assets` links these immutable collections for use by any home. Authoring coordinates are feet; Blender geometry is stored in meters with Z up. Plant origins are at grade, cabinetry origins are at floor center with the front toward -Y, and the paver's top face is at Z=0.

| Key | Versioned asset | Placement |
| --- | --- | --- |
| `grass` | `landscape/ornamental-grass-clump/v002` | Smooth curved grass blades; modest natural scale variation |
| `shrub` | `landscape/sage-shrub/v002` | Nominal three-foot shrub with connected branches and attached leaves |
| `olive` | `landscape/olive-tree/v001` | Nominal fourteen-foot olive; illustrative planting |
| `paver` | `surfaces/honed-limestone-paver-4ft/v001` | 4 x 4 feet, 1.2-inch thickness; 4.02-foot pitch gives 0.24-inch joints |
| `wardrobe` | `cabinetry/oak-wardrobe-2ft/v001` | 2 x 2 x 8 feet; pulls add 0.094 feet beyond front |
| `base_cabinet` | `cabinetry/oak-drawer-base-2ft/v001` | 2 x 2 x 2.86 feet nominal; continuous counter supplied by host |
| `oven` | `appliances/built-in-oven-30in/v001` | 30W x 24D x 28H inches nominal; bottom center, front -Y, handle proud |
| `dishwasher` | `appliances/dishwasher-24in/v001` | 24W x 24D x 34H inches nominal; floor center, front -Y, handle proud |
| `cooktop` | `appliances/induction-cooktop-36in/v001` | 36W x 21D inches; top glass at Z=0; controls toward -Y |
| `hood` | `appliances/wall-hood-36in/v001` | 36W x 22D x 30H inches nominal; bottom center, rear +Y toward wall |
| `fireplace` | `fixtures/closed-glass-fireplace-48in/v001` | 48W x 18D x 32H inches nominal plus flue collar; bottom center, front -Y |
| `fridge` | `appliances/panel-ready-fridge-48in/v001` | 48W x 30D x 84H inches nominal; floor center, front -Y; oak door panels |
| `bathtub` | `fixtures/freestanding-tub-72in/v001` | 72L alongX x36W alongY x24H inches; floorcenter; hollowbasin |
| `toilet` | `fixtures/toilet-elongated/v001` | Nominal 16W × 30D inch plan envelope; floor center, front -Y; raised lid about 39 inches high |
| `downlight` | `fixtures/lighting-recessed-downlight-3in/v001` | Ceiling plane origin; requires an actual cutout and service cavity |
| `taskbar` | `fixtures/lighting-undercabinet-bar-4ft/v001` | Cabinet underside origin; 48-inch long axis X |
| `linear_pendant` | `fixtures/lighting-linear-pendant-4ft/v001` | Ceiling canopy origin; bottom approximately31.85inches below |

```python
from common.shared_assets import load_catalog, place, dependencies
shared = load_catalog(ROOT, keys=['grass', 'paver', 'wardrobe'])
place('Bedroom wardrobe bay 1', shared['wardrobe'], (20, 12, 0))
place('Patio paver', shared['paver'], (2, 42, -.08))
place('Garden grass', shared['grass'], (-4, 20, local_grade), rotation=.7, scale=.9)
# Append to the home's asset_dependencies; these paths are relative to its folder.
pins = dependencies(ROOT, keys=['grass', 'paver', 'wardrobe'])
```

The cabinet modules reference the existing white-oak material; paving references the existing honed limestone. Local home generators do not recreate those material nodes. All geometry and leaf shapes are original project work, with no external textures or commercial models. Source code is MIT; original designs/assets use CC BY 4.0 with attribution to Homes project contributors.

From the repository root, use Blender 4.5.14 LTS:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/library/publish_shared.py
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/library/verify_shared.py -- --render
```

Each version contains its actual editable collection, a manifest, and a native Blender preview. The verifier reopens every file, resolves its linked materials within the repository, and compares evaluated bounds with the manifest. Its current receipt is `shared-validation.json`.

The original appliances include actual modeled details: oven cavity and wire racks behind glazing, controls and handles, induction zones, hood baffles and chimney cover. They are generic planning envelopes, not selected commercial products. Host designs must remove solid cabinet geometry from the oven/dishwasher openings and supply the hood exhaust and fireplace flue routes. The fireplace is shown unlit; fuel type, listed product, hearth and combustible clearances are not selected.

Lighting collections are also registered here for discovery and dependency pins. Use `common.lighting_assets.place` when placing working illumination: it supplies a host-owned light source with per-instance power. `common.shared_assets.place` places fixture geometry only. Publish lighting through `tools/library/publish_lighting.py`; read its manifests for the exact mounting and cutout requirements.

To refresh only new appliance previews while retaining the native checks for every catalog entry:

```sh
/Applications/Blender.app/Contents/MacOS/Blender --background --python-exit-code 1 --python tools/library/verify_shared.py -- --render --keys oven,dishwasher,cooktop,hood,fireplace
```
