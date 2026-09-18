# Shared asset catalog

Original project components are stored here with explicit version pins. Homes link the actual Blender collections and materials; updates create a new version rather than changing geometry underneath another home.

## Plants, paving and storage

These are native Blender renders of the reusable source files. Each manifest records measured dimensions, origin, authoring source, license and relative dependencies.

| Curved ornamental grass · v002 | Connected sage shrub · v002 | Original olive tree · v001 |
| --- | --- | --- |
| [![Ornamental grass](landscape/ornamental-grass-clump/v002/preview.png)](landscape/ornamental-grass-clump/v002/asset.json) | [![Sage shrub](landscape/sage-shrub/v002/preview.png)](landscape/sage-shrub/v002/asset.json) | [![Olive tree](landscape/olive-tree/v001/preview.png)](landscape/olive-tree/v001/asset.json) |
| Base at grade; modest natural variation | Base at grade; attached leaves and branches | Nominal fourteen-foot ornamental tree |

| Four-foot limestone paver · v001 | Two-foot wardrobe bay · v001 | Two-foot drawer cabinet · v001 |
| --- | --- | --- |
| [![Limestone paver](surfaces/honed-limestone-paver-4ft/v001/preview.png)](surfaces/honed-limestone-paver-4ft/v001/asset.json) | [![Oak wardrobe](cabinetry/oak-wardrobe-2ft/v001/preview.png)](cabinetry/oak-wardrobe-2ft/v001/asset.json) | [![Oak base cabinet](cabinetry/oak-drawer-base-2ft/v001/preview.png)](cabinetry/oak-drawer-base-2ft/v001/asset.json) |
| 4 × 4 ft, 1.2 in thick; top at Z=0 | 2 × 2 × 8 ft; shelf, rail, doors and handles | 2 × 2 × 2.86 ft; continuous worktop supplied by home |

Cabinet fronts face -Y and their origins are at floor center. The wardrobe's pulls extend 0.094 feet beyond its nominal depth. Paving uses a deliberate placement pitch for joints; do not stretch the tile. Plant selection is illustrative, with no claim about suitability for a specific site.

See the [shared component API and regeneration instructions](../tools/library/README.md). The current native reopen, dependency and dimension checks are recorded in [shared validation](../tools/library/shared-validation.json). Preview review replaced the first grass and shrub drafts with v002; v001 remains immutable for any existing links.

## Materials, fixtures and furniture

| Asset | Category | Placement / scale | Used by |
|---|---|---|---|
| [Sage fluted ceramic](materials/sage-fluted-tile/v001/asset.json) | Material + tile geometry | 3 × 12 in nominal module, including grout | Atrium 01, Timber Courtyard 02 |
| [Opal globe pendant](fixtures/opal-globe-pendant/v001/asset.json) | Fixture collection | Origin at ceiling mount; geometry extends down | Promoted from Atrium 01; linked by Timber Courtyard 02 |
| [Walnut counter stool](furniture/walnut-counter-stool/v001/asset.json) | Furniture collection | Floor origin under seat; approx. 24.6 in seat height | Promoted from Atrium 01; linked by Timber Courtyard 02 |
| [Warm vertical cedar](materials/warm-vertical-cedar/v001/asset.json) | Procedural material | Intended for 6 in board modules | Timber Courtyard 02 |
| [Charcoal standing-seam metal](materials/charcoal-standing-seam/v001/asset.json) | Procedural material | Intended for 12 in seam spacing | Timber Courtyard 02 |

Open or link the `.blend` file next to each manifest. Tile and fixture assets are collections; cedar and metal are material datablocks. The material assets do not generate geometry by themselves: reusable geometry helpers and the home's generator create the matching boards and seams.

The procedural helpers in `tools/common/landscape.py` remain available for authoring new assets. Repeated plant geometry in homes should use the linked collections above, rather than regenerating a private copy for each project.

Read [asset conventions](../docs/assets.md) before adding or changing an asset. Preserve local coordinates when linking collections, especially curve-based objects.

## Garage Loft additions

- [Double pit parking carriage v002](fixtures/double-pit-parking-carriage/v002/asset.json): original two-level, double-width schematic equipment proxy. References KLAUS planning dimensions; not manufacturer CAD or installation documentation.
- [Walnut eight-foot pool table v002](furniture/walnut-eight-foot-pool-table/v002/asset.json): original furniture with a 44 x 88 inch playing area.
- [Warm vertical cedar v002](materials/warm-vertical-cedar/v002/asset.json): refined original timber shader. Earlier homes retain their explicit v001 links.

## Coastal palette

- [Natural white oak v001](materials/coastal-white-oak/v001/asset.json): physical-scale original wood grain, also linked by the shared cabinets.
- [Honed limestone v001](materials/coastal-honed-limestone/v001/asset.json): fine original mineral shader, also linked by the shared paving module.
- [Oak counter stool v001](furniture/coastal-oak-counter-stool/v001/asset.json): original upholstered counter-height seat with curved timber back, linked oak and metal footrest.

Original assets use CC BY 4.0 with attribution to Homes project contributors; generators use MIT. No collection above is manufacturer CAD or a certification of building/product compliance.

## Complete kitchen and bathing components

These original editable appliances are shared across projects. The host home supplies appliance openings, accessible operating space, plumbing, electrical services and a continuous hood exhaust route. Nominal widths are given below; measured dimensions including handles are in each manifest.

| Integrated 48-inch oak refrigerator | 30-inch built-in oven | 36-inch wall hood |
| --- | --- | --- |
| [![Integrated oak refrigerator](appliances/panel-ready-fridge-48in/v001/preview.png)](appliances/panel-ready-fridge-48in/v001/asset.json) | [![Built-in oven](appliances/built-in-oven-30in/v001/preview.png)](appliances/built-in-oven-30in/v001/asset.json) | [![Wall hood](appliances/wall-hood-36in/v001/preview.png)](appliances/wall-hood-36in/v001/asset.json) |
| Shared oak panels, narrow reveals, recessed grille | Actual glass, inner cavity, racks and controls | Canopy, baffles, task lenses and chimney cover |

| 24-inch dishwasher | 36-inch induction cooktop | 72-inch freestanding bathtub |
| --- | --- | --- |
| [![Dishwasher](appliances/dishwasher-24in/v001/preview.png)](appliances/dishwasher-24in/v001/asset.json) | [![Induction cooktop](appliances/induction-cooktop-36in/v001/preview.png)](appliances/induction-cooktop-36in/v001/asset.json) | [![Hollow freestanding bathtub](fixtures/freestanding-tub-72in/v001/preview.png)](fixtures/freestanding-tub-72in/v001/asset.json) |
| Separate appliance bay; keep open-door route clear | Five modeled zones; worktop opening supplied by home | Real concave basin, rolled rim and drain |

[![Closed-glass fireplace insert](fixtures/closed-glass-fireplace-48in/v001/preview.png)](fixtures/closed-glass-fireplace-48in/v001/asset.json)

The original **48-inch closed-glass fireplace insert** has an unlit log bed and a conceptual flue collar. The home must provide a noncombustible surround and a continuous flue concept; selected fuel, listed equipment, hearth and clearance requirements are unresolved.

## Bathroom sanitation fixture

[![Original elongated toilet](fixtures/toilet-elongated/v001/preview.png)](fixtures/toilet-elongated/v001/asset.json)

The shared elongated toilet has a continuous floor-mounted ceramic pedestal, a hollow bowl, an open oval seat and a raised lid. Its measured plan bounds fit a nominal 16 × 30 inch envelope; the raised lid reaches approximately 39 inches above the floor. The floor-center origin faces -Y. Fresh native checks verify the bowl opening and lid travel; each home separately records placement, standing space, door operation and unresolved product/plumbing requirements.

## Mountain materials and planting

- [Neutral brown cedar v003](materials/warm-vertical-cedar/v003/asset.json): per-board tone and growth grain, physical-meter mapping along each member, matte finish. Explicitly adopted by Mountain House; earlier cedar pins remain unchanged.
- [Mountain thermo-ash v002](materials/mountain-thermo-ash/v002/asset.json): deeper brown decking with fine fibers and irregular growth lines, shared independently of the house geometry.
- [Mountain conifer v002](landscape/mountain-conifer/v002/asset.json): original fir collection with trunk-base placement origin, suitable for instanced forest compositions.

| Neutral brown cedar | Deeper thermo-ash |
| --- | --- |
| [![Cedar grain sample](materials/warm-vertical-cedar/v003/preview.png)](materials/warm-vertical-cedar/v003/asset.json) | [![Thermo-ash grain sample](materials/mountain-thermo-ash/v002/preview.png)](materials/mountain-thermo-ash/v002/asset.json) |

## Hardware and lighting options

[Hardware gallery](hardware/README.md): five families in bronze, black and steel, with actual mounting directions and recess requirements.

| Recessed downlight | Task strip | Linear focal pendant |
| --- | --- | --- |
| [![Downlight](fixtures/lighting-recessed-downlight-3in/v001/preview.png)](fixtures/lighting-recessed-downlight-3in/v001/asset.json) | [![Task strip](fixtures/lighting-undercabinet-bar-4ft/v001/preview.png)](fixtures/lighting-undercabinet-bar-4ft/v001/asset.json) | [![Linear pendant](fixtures/lighting-linear-pendant-4ft/v001/preview.png)](fixtures/lighting-linear-pendant-4ft/v001/asset.json) |

The recessed fixture needs a real ceiling opening and service cavity. Hosts choose actual lamp power/controls; these are original visual concepts without rated photometry. [Placement guidance](../tools/library/lighting.md).

[Reuse, adapt and contribute](../docs/assets.md) explains how to preserve adopted versions, record derivation, publish reviewed variations and explicitly adopt them in a home.
