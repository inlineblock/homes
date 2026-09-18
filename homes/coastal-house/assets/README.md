# Coastal asset inventory and actual adoption

The saved scene links these portable library versions rather than embedding copies:

| Component | Shared asset | Version | Actual use |
| --- | --- | --- | --- |
| White oak | materials/coastal-white-oak | v001 | Interior joinery, roof fascia, furniture and carport |
| Honed limestone | materials/coastal-honed-limestone | v001 | Floor, terrace and facade finishes |
| Counter stool | furniture/coastal-oak-counter-stool | v001 | Island and exterior serving counter |
| Opal pendant | fixtures/opal-globe-pendant | v001 | Entry lighting |
| Ornamental grass | landscape/ornamental-grass-clump | v002 | Dunes, border and front planting drifts |
| Sage shrub | landscape/sage-shrub | v002 | Front and rear landscape |
| Olive tree | landscape/olive-tree | v001 | Site framing and background canopy |
| Limestone paver | surfaces/honed-limestone-paver-4ft | v001 | 72 terrace paver instances, 4.02 ft spacing |
| Oak wardrobe | cabinetry/oak-wardrobe-2ft | v001 | Thirteen bays: six guest, three dressing, two pantry, one coat and one linen |

Additional adopted v001 assets: appliances/built-in-oven-30in, dishwasher-24in, induction-cooktop-36in, wall-hood-36in and panel-ready-fridge-48in; fixtures/freestanding-tub-72in, toilet-elongated, lighting-recessed-downlight-3in and lighting-undercabinet-bar-4ft; hardware/bar-pull-satin-bronze and door-lever-satin-bronze.

All twenty direct libraries reopen from relative paths. Asset metadata records real scale, placement, source, rights and nested material dependencies. Plants permit controlled scale/rotation variation; pavers and wardrobes retain their published dimensions.

Bespoke kitchen layout, opening pockets, roof, carport and terrain remain in `tools/coastal04/`. Generic furniture and physical-scale finish helpers are shared through `tools/common/`; original unbranded passenger cars reuse `tools/garage03/cars.py`. There are no downloaded meshes or private opaque asset copies. This revision does not adopt the separate shared base-cabinet asset: its existing serving cabinetry is a bespoke full-width assembly with a continuous sill/counter detail.

Original design/asset license: CC BY 4.0. Authoring code: MIT.
