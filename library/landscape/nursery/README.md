# Comparative plant nursery

A linked Blender placement demonstration of all 35 new plant families, separated into six labeled beds. These climate tags are browse groups: this is not a proposed garden that combines incompatible growing conditions.

The native scene links one representative variant per family. Every family file also contains its other two variants. Plant origins remain at planting grade Z=0; spacing uses measured canopy bounds with at least one meter between adjacent planting cells. Gravel paths stay outside the beds.

This demonstrates linked placement and portability. It does not adopt these assets into any existing home or establish horticultural suitability, root-zone sizing, irrigation or mature spacing.

## Cameras

| Bed | Native camera |
|---|---|
| Mountain | `Nursery_mountain` |
| Desert | `Nursery_desert` |
| Xeric | `Nursery_xeric` |
| Coastal | `Nursery_coastal` |
| Suburban | `Nursery_suburban` |
| Fruit | `Nursery_fruit` |
| Whole nursery | `Nursery_overview` |

Scene: [nursery.blend](nursery.blend). Fresh-process geometry and relative-link checks: [validation.json](validation.json). Native images are generated separately after reopening this scene.

Source: [nursery.py](../../../tools/library/plants/nursery.py). Run its `--verify` mode in a separate Blender process after building.

All geometry/materials are original. Plant assets: CC BY 4.0, attribution Homes project contributors. Authoring code: MIT.

## Native placement gallery

Actual renders of the linked nursery scene. These demonstrate geometry and planting contact in separate comparative beds; they are not Image Gen interpretations.

### Overview

![Overview comparative planting bed](overview.png)

### Mountain

![Mountain comparative planting bed](mountain.png)

### Desert

![Desert comparative planting bed](desert.png)

### Xeric

![Xeric comparative planting bed](xeric.png)

### Coastal

![Coastal comparative planting bed](coastal.png)

### Suburban

![Suburban comparative planting bed](suburban.png)

### Fruit

![Fruit comparative planting bed](fruit.png)

Final visual review: all six group views and the overview passed. Small plants are visible in front of taller specimens; native reopening and source hashes are recorded in [validation.json](validation.json).
