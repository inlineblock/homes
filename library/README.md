# Shared asset catalog

Original project components are stored here with explicit version pins. Homes link the actual Blender collections and materials; updates create a new version rather than changing geometry underneath another home.

[Landscape plant gallery](landscape/gallery.md): **35 new built families and 105 named variants**, across mountain, desert, water-wise, coastal, suburban and fruit-tree groups. [Selection notes](landscape/README.md), [catalog data](landscape/catalog.json), and a [linked comparative nursery](landscape/nursery/README.md) sit beside the models. All 35 new families passed native reopen/link checks and whole/detail image review for architectural concept landscaping; they retain simplified botanical geometry rather than photoreal foreground macro detail. Reviews and source/image hashes are recorded per asset. Existing-home adoption remains separate, and the six existing families remain unchanged.

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

## Inset kitchen kit

**[Browse the 27-part inset kitchen kit](kitchen-inset-kit.md)**: 12 cream/oak cabinet modules, five appliances, seven hardware/fixture assemblies and three finishes, all at v001. The catalog includes measured sizes, manifests, native previews and open/service states. Asset reopening and isolated visual reviews are complete; Modern Block’s selected components also passed [host installation checks](../homes/modern-block/model/kitchen-validation.json). These are original reusable concepts, not commercial product specifications.

| Cream appliance garage · open | Concealed 48-inch refrigerator/freezer | Brass double-shade pendant · 1.35 m drop |
| --- | --- | --- |
| [![Cream inset appliance garage with bifolding doors open](cabinetry/cream-inset-appliance-garage-48in/v001/preview-open.png)](cabinetry/cream-inset-appliance-garage-48in/v001/asset.json) | [![Cream inset refrigerator/freezer with long brass pulls](appliances/cream-inset-fridge-freezer-48in/v001/preview.png)](appliances/cream-inset-fridge-freezer-48in/v001/asset.json) | [![Brass double-shade pendant with extended solid suspension stem](fixtures/lighting-brass-double-shade-pendant/v001/preview.png)](fixtures/lighting-brass-double-shade-pendant/v001/asset.json) |

## Complete kitchen and bathing components

These original editable appliances are shared across projects. The host home supplies appliance openings, accessible operating space, plumbing, electrical services and a continuous hood exhaust route. Nominal widths are given below; measured dimensions including handles are in each manifest.

**[Explore the cooking and appliance gallery](appliances/README.md)** for integrated induction/gas/dual-fuel ranges, separate cooktops, single/double ovens, oven/speed-oven combinations and coordinated paneled appliances. Choose a range **or** a cooktop plus explicit oven; then coordinate extraction, services, landing space and real cabinet/pantry storage. Every linked option includes native sources and measured interfaces. Asset review does not establish installation fit in a home.

| 36-inch induction range | 48-inch dual-fuel range | 30-inch double wall oven |
| --- | --- | --- |
| [![36-inch induction range with five zones and oven](appliances/induction-range-36in/v001/preview.png)](appliances/induction-range-36in/v001/asset.json) | [![48-inch dual-fuel range with two ovens](appliances/dual-fuel-range-48in/v001/preview.png)](appliances/dual-fuel-range-48in/v001/asset.json) | [![30-inch double wall oven](appliances/double-wall-oven-30in/v001/preview.png)](appliances/double-wall-oven-30in/v001/asset.json) |
| One electric oven + induction surface | Six gas burners, electric griddle + two electric ovens | Two full cavities; tall housing and operating reach remain host decisions |

Also available: [30-inch induction range](appliances/induction-range-30in/v001/asset.json), [36-inch gas range](appliances/gas-range-36in/v001/asset.json), [30-inch oven/speed-oven combination](appliances/oven-speed-oven-combo-30in/v001/asset.json), [30-inch induction cooktop](appliances/induction-cooktop-30in/v001/asset.json) and [36-inch gas cooktop](appliances/gas-cooktop-36in/v001/asset.json). The [full gallery](appliances/README.md) shows every option, its review status, and open/service views where modeled. Existing versions below remain available unchanged.

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

### Smoked-oak kitchen storage and cleanup

Five reusable cabinet modules and coordinated paneled appliances make actual storage, appliance openings and cleanup equipment available to each home. These are original concept assets with inspected native previews and fresh-reopen receipts. Closed-state cabinet and paneled-appliance previews do not prove operating clearance in a home.

| 24-inch drawer base | 36-inch sink base | 36-inch oven housing |
| --- | --- | --- |
| [![Smoked-oak drawer base with bronze hardware](cabinetry/smoked-oak-drawer-base-2ft/v001/preview.png)](cabinetry/smoked-oak-drawer-base-2ft/v001/asset.json) | [![Smoked-oak sink base with plumbing space](cabinetry/smoked-oak-sink-base-36in/v001/preview.png)](cabinetry/smoked-oak-sink-base-36in/v001/asset.json) | [![Smoked-oak oven housing with actual opening](cabinetry/smoked-oak-oven-base-36in/v001/preview.png)](cabinetry/smoked-oak-oven-base-36in/v001/asset.json) |
| Everyday utensils, dishes and cookware | Open service zone; host supplies cut worktop | Supported opening for the existing 30-inch oven; no opaque front over the appliance |

| 18-inch waste pullout | 24-inch pantry shelf | Sink and mixer · v002 |
| --- | --- | --- |
| [![Smoked-oak waste pullout cabinet](cabinetry/smoked-oak-waste-pullout-18in/v001/preview.png)](cabinetry/smoked-oak-waste-pullout-18in/v001/asset.json) | [![Smoked-oak open pantry shelving](cabinetry/smoked-oak-pantry-shelf-2ft/v001/preview.png)](cabinetry/smoked-oak-pantry-shelf-2ft/v001/asset.json) | [![Shared kitchen sink and mixer](fixtures/kitchen-sink-mixer-650/v002/preview.png)](fixtures/kitchen-sink-mixer-650/v002/asset.json) |
| Plan front travel and standing space | 24 × 12 × 84 in nominal; shallow accessible shelving | Corrected 664 × 464 mm concept cutout; unchanged parent geometry |

| 48-inch paneled refrigerator | 24-inch paneled dishwasher |
| --- | --- |
| [![Smoked-oak wide refrigerator](appliances/smoked-oak-panel-ready-fridge-48in/v001/preview.png)](appliances/smoked-oak-panel-ready-fridge-48in/v001/asset.json) | [![Smoked-oak integrated dishwasher](appliances/smoked-oak-panel-ready-dishwasher-24in/v001/preview.png)](appliances/smoked-oak-panel-ready-dishwasher-24in/v001/asset.json) |

Cabinet bodies use floor-center origins and front −Y. Bronze pulls project beyond nominal case depth; hosts supply a continuous worktop with real appliance/sink cutouts. The sink v002 manifest corrects the cutout allowance while preserving v001. Read each exact version's dimensions and operating assumptions; do not treat nominal cabinet width as an appliance opening. [Selection and contribution workflow](../docs/assets.md).

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

| Satin-bronze duplex power outlet |
| --- |
| [![Satin-bronze duplex outlet with ivory receptacles and actual plug apertures](fixtures/duplex-power-outlet-bronze/v001/preview.png)](fixtures/duplex-power-outlet-bronze/v001/asset.json) |

The original [duplex outlet v001](fixtures/duplex-power-outlet-bronze/v001/asset.json) has a 2.75 × 4.5 inch faceplate, actual blade/ground apertures and a hollow recessed box. Its origin is at the finished wall plane, facing −Y; a horizontal placement rotates the plate and required cavity together. [Fresh native and preview review](fixtures/duplex-power-outlet-bronze/v001/validation.json) verifies the isolated asset. Hosts must create the actual opening and reserve accessible plug/cord space, especially at kitchen and pantry appliance worktops. This visual location concept supplies no electrical rating, listing, protection specification or code approval.

[Reuse, adapt and contribute](../docs/assets.md) explains how to preserve adopted versions, record derivation, publish reviewed variations and explicitly adopt them in a home.

## Lindon collection — brick, windows, rooms and outdoor living

Eighteen new **v001** assets make the Lindon concept's components available to other homes. The previews below are native renders of the reusable source files. They show available geometry and materials; installation, circulation and operating clearances still need review in each adopting home.

| Warm red running-bond brick | Slim dark window | Linen three-seat sofa |
| --- | --- | --- |
| [![Warm red brick with running bond and mortar joints](materials/warm-red-brick/v001/preview.png)](materials/warm-red-brick/v001/asset.json) | [![Dark three-panel window in a sample wall opening](openings/slim-dark-window/v001/preview.png)](openings/slim-dark-window/v001/asset.json) | [![Linen three-seat sofa with separate cushions](furniture/linen-three-seat-sofa/v001/preview.png)](furniture/linen-three-seat-sofa/v001/asset.json) |

| Rectangular pool | Pickleball court | Slatted outdoor chaise |
| --- | --- | --- |
| [![Rectangular pool with coping and submerged entry steps](fixtures/rectangular-pool-6x12m/v001/preview.png)](fixtures/rectangular-pool-6x12m/v001/asset.json) | [![Pickleball playing surface with lines and net](surfaces/pickleball-court-30x60ft/v001/preview.png)](surfaces/pickleball-court-30x60ft/v001/asset.json) | [![Slatted timber chaise with fixed reclining back and cushion](furniture/slatted-outdoor-chaise/v001/preview.png)](furniture/slatted-outdoor-chaise/v001/asset.json) |

Each link below opens the exact version's dimensions, origin, dependencies, source and installation notes. More previews and the editable `.blend` sit beside each manifest.

| Family | Available v001 assets | Scale and placement notes |
| --- | --- | --- |
| Facade | [Warm red brick](materials/warm-red-brick/v001/asset.json) · [Slim dark window](openings/slim-dark-window/v001/asset.json) | Brick module pitch 225 × 75 mm, including joints; physical-meter facade mapping also supports angled walls. Window nominal opening 2.4 × 2.4 m with 55 mm frame sightlines; closed concept state. |
| Living | [Linen sofa](furniture/linen-three-seat-sofa/v001/asset.json) · [Rounded oak coffee table](furniture/oak-rounded-coffee-table/v001/asset.json) | Sofa approximately 3.47 m wide; coffee table approximately 1.68 × 0.85 m. Reserve seated access and through routes separately from object bounds. |
| Dining | [Eight-foot oak table](furniture/oak-dining-table-8ft/v001/asset.json) · [One-meter round table](furniture/oak-round-dining-table-1000/v001/asset.json) · [Upholstered oak chair](furniture/oak-upholstered-dining-chair/v001/asset.json) | Long-table and compact round-table choices use separate assets. Chairs need occupied/pulled-back clearance in the host room. |
| Bedrooms and work | [King bed](furniture/oak-linen-king-bed/v001/asset.json) · [Queen bed](furniture/oak-linen-queen-bed/v001/asset.json) · [Open nightstand](furniture/oak-open-nightstand/v001/asset.json) · [Writing desk](furniture/oak-writing-desk/v001/asset.json) | Beds have distinct frame widths and their own measured envelopes; do not stretch one into the other. Desk top is 1.8 × 0.75 m. |
| Kitchen, bath and laundry | [Sink and mixer](fixtures/kitchen-sink-mixer-650/v001/asset.json) · [Basin, mixer and mirror](fixtures/vanity-basin-mixer-mirror/v001/asset.json) · [900 mm shower tray/screen](fixtures/shower-tray-screen-900/v001/asset.json) · [600 mm laundry module](appliances/front-loading-laundry-600/v001/asset.json) | Counter-mounted fixtures use the mounting plane as Z=0; other modules stand at floor level. Hosts provide actual cutouts, support, wet-area detailing, services and access. Laundry door is modeled closed. |
| Pool and terrace | [Rectangular pool](fixtures/rectangular-pool-6x12m/v001/asset.json) · [Slatted chaise](furniture/slatted-outdoor-chaise/v001/asset.json) | Pool water footprint 6 × 12 m; shell extends below the host deck datum. Chaise is 0.72 × 1.98 m with fixed recline. These are reusable concept sizes, not measurements of the listed property. |
| Court | [Pickleball court](surfaces/pickleball-court-30x60ft/v001/asset.json) | 20 × 44 ft markings on a 30 × 60 ft surface. Host supplies suitable base, drainage, perimeter safety and site fit; modeled dimensions do not certify an installed facility. |

These are original Homes project assets under **CC BY 4.0**, with attribution to Homes project contributors; authoring code is MIT. They contain no listing photographs or source floor-plan graphics. Interior oak furniture pins the existing `coastal-white-oak/v001` material; the window links `bar-pull-matte-black/v001` as a conceptual grip, not a specified casement lock. Product selection and host validation remain separate from asset publication.

**Reuse → adapt → contribute:** choose an asset that fits, link its exact version, and verify it in the home. For a different size or design, preserve the adopted source, publish a versioned variation or distinct sibling with its derivation and preview, then explicitly adopt it. Keep the home's asset schedule aligned with actual links. [Full selection and contribution workflow](../docs/assets.md).

## Coordinated red-brick exterior palette

The Lindon styling review contributed nine additional versioned options. Only explicitly adopted pins change in a home. Neutral native previews and fresh-link receipts sit alongside each asset; host daylight and material proportions still require review.

| Deep iron red — Lindon adoption | Lighter russet option | Warm matte charcoal roof |
| --- | --- | --- |
| [![Deep iron red brick](materials/warm-red-brick/v003/preview.png)](materials/warm-red-brick/v003/asset.json) | [![Lighter muted red brick](materials/warm-red-brick/v002/preview.png)](materials/warm-red-brick/v002/asset.json) | [![Warm charcoal roofing](materials/charcoal-standing-seam/v002/preview.png)](materials/charcoal-standing-seam/v002/asset.json) |

| Charcoal facade panel | Warm limestone plaster | Smoked oak |
| --- | --- | --- |
| [![Charcoal facade panel](materials/charcoal-facade-panel/v001/preview.png)](materials/charcoal-facade-panel/v001/asset.json) | [![Warm limestone plaster](materials/warm-limestone-plaster/v001/preview.png)](materials/warm-limestone-plaster/v001/asset.json) | [![Smoked oak grain](materials/smoked-oak/v001/preview.png)](materials/smoked-oak/v001/asset.json) |

| Slim bronze glazing | Flowering perennial clump |
| --- | --- |
| [![Slim bronze window](openings/slim-dark-window/v002/preview.png)](openings/slim-dark-window/v002/asset.json) | [![Lilac and ivory flowering perennial](landscape/flowering-perennial-clump/v001/preview.png)](landscape/flowering-perennial-clump/v001/asset.json) |

Brick preserves physical 225 × 75 mm coursing. Window v002 has 40 mm nominal frame sightlines and neutral double glazing; nonuniform host scaling changes those dimensions. The perennial is original reusable geometry, not a specified or climate-approved plant species. The current Lindon pins use the darker v003 brick; v001/v002 and all other homes' choices remain intact.

[![Subdued mushroom mineral plaster](materials/mushroom-mineral-plaster/v001/preview.png)](materials/mushroom-mineral-plaster/v001/asset.json)

The [mushroom mineral plaster option](materials/mushroom-mineral-plaster/v001/asset.json) provides a substantially darker, low-chroma warm gray-brown alternative to the limestone plaster above. Its actual neutral CPU preview and fresh native reopening were reviewed; hosts separately check sun/shade response beside brick and charcoal. The original limestone material remains available unchanged.

## Coastal comfort collection

Coastal House links these original v001 furnishings and textiles. Native previews, exact dimensions, placement and concept operating clearances are recorded in each manifest. These are original designs, not specified commercial products.

| Timber outdoor sofa | Matching lounge chair |
| --- | --- |
| [![Outdoor sofa](furniture/coastal-outdoor-sofa/v001/preview.png)](furniture/coastal-outdoor-sofa/v001/asset.json) | [![Outdoor lounge chair](furniture/coastal-outdoor-lounge-chair/v001/preview.png)](furniture/coastal-outdoor-lounge-chair/v001/asset.json) |

| Woven oatmeal rug | Olive linen cushion |
| --- | --- |
| [![Bound woven rug](furniture/woven-oatmeal-rug/v001/preview.png)](furniture/woven-oatmeal-rug/v001/asset.json) | [![Olive cushion](furniture/olive-linen-cushion/v001/preview.png)](furniture/olive-linen-cushion/v001/asset.json) |

Shared material assets: [woven oatmeal](materials/woven-oatmeal/v001/asset.json), [olive linen](materials/olive-linen/v001/asset.json) and existing [smoked oak](materials/smoked-oak/v001/asset.json). Regenerate through `tools/library/publish_coastal_comfort.py`; published versions remain immutable.

## Driftwood coastal pavilion collection

Coastal House adopts these reusable variations alongside existing mushroom plaster and limestone. Source versions are preserved. Each folder includes its native file, measured or shader contract, preview and verification.

| Driftwood timber | Matte bronze-gray roofing | Large limestone wall panel | Vault pendant |
| --- | --- | --- | --- |
| [![Driftwood timber](materials/coastal-driftwood/v001/preview.png)](materials/coastal-driftwood/v001/asset.json) | [![Bronze-gray metal](materials/bronze-gray-standing-seam/v001/preview.png)](materials/bronze-gray-standing-seam/v001/asset.json) | [![Four by two limestone panel](surfaces/honed-limestone-wall-panel-4x2/v001/preview.png)](surfaces/honed-limestone-wall-panel-4x2/v001/asset.json) | [![Vault pendant](fixtures/lighting-linear-pendant-4ft-vault-3in12/v001/preview.png)](fixtures/lighting-linear-pendant-4ft-vault-3in12/v001/asset.json) |

Timber uses physical-meter grain oriented along actual members. The stone panel is 4 x 2 ft and 1.5 in thick; use rigid full-panel instances or documented real mesh perimeter cuts. The 4 ft pendant has a 90-inch drop and three mount faces for a 3:12 ceiling; do not stretch the original short-drop version. Review host contact, use and material response separately from reusable-asset validation.

See [Coastal House adoption and host checks](../homes/coastal-house/assets/README.md) for these four assets in the model; the isolated asset receipts do not establish suitability in every future house.

## Modern Block courtyard components

Three original reusable **v001** assemblies provide a spreading tree, operable screen leaf and compact courtyard pool. The images are inspected native CPU renders. The previews establish available geometry; installation and operating clearances still require review in the adopting home.

| Broad spreading oak-like tree | Timber center-pivot screen | Four by eight meter pool |
| --- | --- | --- |
| [![Broad spreading tree with attached branches and dark green folded leaves](landscape/broad-canopy-oak/v001/preview.png)](landscape/broad-canopy-oak/v001/asset.json) | [![Timber pivot screen with perimeter frame and separate vertical louvers](openings/timber-pivot-louver-1800x3000/v001/preview.png)](openings/timber-pivot-louver-1800x3000/v001/asset.json) | [![Hollow courtyard pool with below-deck water and submerged steps](fixtures/courtyard-pool-4x8m/v001/preview.png)](fixtures/courtyard-pool-4x8m/v001/asset.json) |

The tree spans approximately **9.36 × 10.14 m**, with its crown about **7.37 m above grade**. Its origin is the trunk at grade; root flare extends slightly below grade. It is an original botanical illustration without species or site-suitability claims. The screen frame is **1.8 × 3.0 m** with 22 actual blades, linked cedar v003 and a centered vertical pivot; rotate the collection instance up to 90 degrees and reserve the recorded 0.903 m swept radius. The pool has a **4 × 8 m water footprint**, 4.64 × 8.64 m coping bounds, a hollow shell and four entry steps; water sits 130 mm below deck. It derives from the preserved shared 6 × 12 m pool and links limestone v001. Hosts must omit ground and deck within the cavity.

Each manifest pins dimensions, origin, dependencies, rights, source and mounting assumptions. Fresh native opening, fresh linking and dependency checks are recorded alongside the assets. Reproduce with `tools/library/publish_modern_block.py`; authoring code is MIT and original asset geometry is CC BY 4.0, attributed to Homes project contributors. See [Modern Block's adoption schedule](../homes/modern-block/assets/README.md) for actual installation evidence.

### Larger shower and open pantry shelving

| Fixed 1500 × 1200 mm shower | Two-foot open shelving bay |
| --- | --- |
| [![Large shower tray, fixed left screen and full-size plumbing fittings](fixtures/shower-tray-screen-1500x1200/v001/preview.png)](fixtures/shower-tray-screen-1500x1200/v001/asset.json) | [![Oak pantry shelving with six open storage tiers](cabinetry/oak-shelving-2ft/v001/preview.png)](cabinetry/oak-shelving-2ft/v001/asset.json) |

The shower is a dedicated dimensional sibling of the 900 mm tray, with original-size fittings and a 1190 mm fixed side screen. Its floor-center origin faces the open entry toward -Y; the host supplies the plumbing wall at +Y, waterproofing and clear approach. The open shelving preserves the two-foot wardrobe carcass and upper shelf, replaces hanging storage with four additional shelf decks, and removes doors and pulls. It is **2 × 2 × 8 ft**, accesses from -Y and pins white oak v001. Both original parent versions remain unchanged. Fresh native opening, linking, dimensions and inspected CPU previews are recorded in each variant's validation file; host access and service checks remain separate. Generator: `tools/library/publish_modern_block_interior.py`.

### Fixed angled cedar privacy screen

[![Native preview of the fixed angled cedar facade screen](openings/angled-cedar-privacy-screen-2000x2800/v001/preview.png)](openings/angled-cedar-privacy-screen-2000x2800/v001/asset.json)

The original **2.0 × 0.30 × 2.8 m** fixed screen uses 23 solid vertical cedar fins at 45° and 84.09 mm pitch, captured by a slim bronze-gray perimeter frame. Its normal-view fin projections overlap; oblique views remain possible. The origin is bottom-center, front is -Y, and only rigid placement is allowed. Cedar v003 and bronze-gray finish v001 are linked exact dependencies. Reserve at least 300 mm behind the frame for concept service access and separately resolve safe cleaning, demountable fixings and operable-window clearance. Fresh native opening, dimensions, linked dependencies and an actual CPU preview are recorded in the asset receipt. Modern Block adopts this assembly as part of its [facade and privacy revision](../homes/modern-block/assets/README.md). Generator: `tools/library/publish_angled_cedar_screen.py`.

## Twin Gables shared details

| Wood-look cover for conceptual steel framing | Closed linen cabinet with real shelves |
| --- | --- |
| [![Hollow wood-look beam cover](assemblies/cedar-steel-beam-cover-300x400/v001/preview.png)](assemblies/cedar-steel-beam-cover-300x400/v001/asset.json) | [![Oak linen cabinet](cabinetry/oak-linen-cabinet-2ft/v001/preview.png)](cabinetry/oak-linen-cabinet-2ft/v001/asset.json) |

The **300 × 400 mm hollow U-cover** is nonstructural, with 20 mm concept finish thickness and a separate cavity for host-owned steel. Only its 1 m stock length may scale along its length axis; its section stays fixed. The manifest records installation gaps, open ends and the wood-grain scaling limitation. Steel design, fire protection, fixings and weather performance remain unresolved.

The **24 × 24 × 96-inch linen cabinet** preserves the shared wardrobe's closed doors and replaces the hanging rail with five storage shelves. Its [open-door native preview](cabinetry/oak-linen-cabinet-2ft/v001/open-preview.png) exposes the actual interior. Both assets have fresh native/link checks and inspected CPU previews; host installation remains a separate check in [Twin Gables Courtyard's asset schedule](../homes/eichler-twin-gables/assets/README.md).

## Warm walnut cabinetry

Atrium 01 adopts an original walnut finish and rigid, versioned derivatives of the existing cabinet and appliance families. The original oak and smoked-oak assets remain unchanged. Each new manifest records its source, dimensions, mounting, operating reservations and exact dependencies; actual native previews and fresh-link checks accompany the assets.

| Walnut drawers | Plumbing-ready vanity | Paneled refrigeration |
| --- | --- | --- |
| [![Walnut drawer base](cabinetry/walnut-drawer-base-2ft/v001/preview.png)](cabinetry/walnut-drawer-base-2ft/v001/asset.json) | [![Walnut vanity base](cabinetry/walnut-vanity-base-24in/v001/preview.png)](cabinetry/walnut-vanity-base-24in/v001/asset.json) | [![Walnut refrigerator](appliances/walnut-panel-ready-fridge-48in/v001/preview.png)](appliances/walnut-panel-ready-fridge-48in/v001/asset.json) |

The collection includes [warm walnut](materials/warm-walnut/v001/asset.json), [sink base](cabinetry/walnut-sink-base-36in/v001/asset.json), [oven base](cabinetry/walnut-oven-base-36in/v001/asset.json), [waste pullout](cabinetry/walnut-waste-pullout-18in/v001/asset.json), [pantry shelving](cabinetry/walnut-pantry-shelf-2ft/v001/asset.json), [wardrobe](cabinetry/walnut-wardrobe-2ft/v001/asset.json), [cleaning cabinet](cabinetry/walnut-cleaning-cabinet-2ft/v001/asset.json), and [paneled dishwasher](appliances/walnut-panel-ready-dishwasher-24in/v001/asset.json). The 720 mm-high vanity has an open plumbing cavity; the host provides the top, basin mounting and actual service routing. Regenerate with `tools/library/publish_atrium_walnut.py`. See [Atrium's adoption and host checks](../homes/atrium-01/assets/README.md).

### Bedroom roller-blind states

Atrium 01 links four original roller-blind sizes, each with separate open and closed native collections: [42 × 78 in](openings/roller-blackout-42in-78in/v001/asset.json), [54 × 78 in](openings/roller-blackout-54in-78in/v001/asset.json), [48 × 107.4 in](openings/roller-blackout-48in-107p4in/v001/asset.json), and [60 × 107.4 in](openings/roller-blackout-60in-107p4in/v001/asset.json). Dimensions describe the glazing bay pitch and full drop. Cassettes retain a 12 mm neighboring gap; opaque woven panels overlap the specified visible glass by 17 mm at each jamb. Native previews and fresh-link checks cover both states. These are generic privacy concepts, not certified blackout products; hosts verify mounting, obstructions, edge light and service access. Generator: `tools/library/publish_roller_blinds.py`.

## Dressing, library wall and utility options

These original components are available as reviewed isolated assets for the compact Twin Gables layout study. They are **not yet adopted in a revised home**; the user is selecting a floor plan first. Actual host fit and operation must be checked after selection.

| Open dressing | Drawers and folded storage | Floor-to-ceiling bookcase | Premium laundry stack |
| --- | --- | --- | --- |
| [![Double hanging bay](cabinetry/oak-open-double-hang-2ft/v001/preview.png)](cabinetry/oak-open-double-hang-2ft/v001/README.md) | [![Drawer and shelf tower](cabinetry/oak-dressing-drawers-shelves-2ft/v001/open-preview.png)](cabinetry/oak-dressing-drawers-shelves-2ft/v001/README.md) | [![Ten-foot bookcase](cabinetry/oak-full-height-bookcase-2ft/v001/preview.png)](cabinetry/oak-full-height-bookcase-2ft/v001/README.md) | [![Washer and dryer stack](appliances/premium-stacked-laundry-596/v001/preview.png)](appliances/premium-stacked-laundry-596/v001/README.md) |

Complete the mixed dressing layout with the [long-hang bay](cabinetry/oak-open-long-hang-2ft/v001/README.md), [shoe tower](cabinetry/oak-shoe-tower-2ft/v001/README.md), [ventilated pullout hamper](cabinetry/oak-ventilated-hamper-2ft/v001/README.md) and [full-length bronze mirror](fixtures/full-length-bronze-mirror-24x72/v001/README.md). The [36-inch open pantry island base](cabinetry/smoked-oak-open-island-base-36in/v001/README.md) provides storage without another moving door or drawer in the work aisle.

Each manifest records actual bounds, origins and operation allowances. Drawer fronts and pulls project beyond nominal carcasses. High bookcase shelves are occasional storage with a safe access method still to be selected, not universally reachable daily storage. The original unbranded laundry stack uses documented manufacturer dimensional precedents; its native geometry is not approved product CAD. Two linked stacks provide four machines. Preserve the installation and operator reservations in its manifest.


## Kitchen sink and backsplash choices

Four original sink assemblies offer different uses; each links the same reusable [pull-down mixer](fixtures/kitchen-pull-down-mixer-315/v001/README.md). Native previews show real bowl, drain and countertop openings. These are reusable concept assets, not selected commercial products or adopted home installations.

| Wide undermount | Workstation with removable accessories | White apron front | Compact prep |
| --- | --- | --- | --- |
| [![Wide stainless bowl](fixtures/wide-undermount-sink-800/v001/preview.png)](fixtures/wide-undermount-sink-800/v001/README.md) | [![Workstation bowl with board and roll mat](fixtures/workstation-sink-860/v001/preview.png)](fixtures/workstation-sink-860/v001/README.md) | [![Apron-front bowl](fixtures/white-apron-front-sink-32in/v001/preview.png)](fixtures/white-apron-front-sink-32in/v001/README.md) | [![Compact prep bowl](fixtures/compact-prep-sink-400/v001/preview.png)](fixtures/compact-prep-sink-400/v001/README.md) |

**Choose the cabinet and sink together.** The manifests record bowl, rim, faucet and service keep-outs. Compatible cabinet assemblies are not supplied: the existing 36-inch sink base's upper rail conflicts with the wider sink, despite its nominal width fitting. Countertop depth, thickness and cutouts must follow the chosen assembly; never force a fit by stretching the bowl or burying its flange. Final hardware, trap/disposal and product templates remain to be coordinated.

| Cream veined slab | Sage stacked fluted tile | Warm ivory handmade-style tile |
| --- | --- | --- |
| [![Slab backsplash with counter junction](surfaces/cream-veined-slab-backsplash-48x24/v001/installation-preview.png)](surfaces/cream-veined-slab-backsplash-48x24/v001/README.md) | [![Sage stacked tile above a counter](surfaces/sage-stacked-backsplash-12x24/v001/installation-preview.png)](surfaces/sage-stacked-backsplash-12x24/v001/README.md) | [![Ivory tile above a counter](surfaces/warm-ivory-handmade-tile-4in/v001/installation-preview.png)](surfaces/warm-ivory-handmade-tile-4in/v001/README.md) |

Backsplash installation specimens show countertop joints and exposed-edge treatment using actual linked finishes. Backing, trims and counter supports in these specimens are illustrative host geometry, not included reusable assemblies. Heat/wet performance and installation suitability depend on selected products. Generators: `tools/library/publish_kitchen_sink_options.py` and `tools/library/publish_backsplash_options.py`; existing versions remain preserved.
