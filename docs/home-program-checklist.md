# Home program and feature checklist

Read this before layout, not after rendering. Use [design standards](home-design-standard.md) for the completion gate and the [design handbook](design-guide/README.md) for selection, climate and building-system decisions. A home is a coordinated place for everyday living, not simply a bedroom/bath count and an attractive facade.

## How agents make decisions

For every project, copy `templates/home/program.md`. Select a brief profile: **comfortable**, **midrange**, **premium**, or **custom luxury**. These are internal design profiles, not legal categories, price promises or universal industry tiers. Every profile must function well; higher tiers buy more choice, space, privacy, durability and detailing rather than permission to omit basics.

For each applicable item record **required / optional / excluded**, **modeled / dimensioned reservation / selected product / engineered / unresolved**, its location, dimensions/clearances, asset ID and version, dependencies and a reason. A reservation is not installed equipment. Do not mark a design reviewed merely because the checklist has text in every row. Inspect the native model, furniture, door operation, plans and images.

User-specific premium defaults here: **double primary vanity, separate shower and bathtub, enclosed toilet room, 42–48-inch wide refrigerator allowance with 48 inches for Coastal and Mountain, cabinet-matched panel-ready refrigerator fronts, thoughtful hardware, recessed/task lighting as the base with intentional decorative focal fixtures**. These preferences guide our briefs, not every real home or jurisdiction. Fireplace is an explicit per-project choice; Mountain includes one, Coastal currently does not.

## Functional inventory

| Area | Required baseline decisions | Premium / optional choices | What agents must check |
|---|---|---|---|
| Site | Actual or explicitly illustrative site, road, grade, orientation, hazards, drainage, utilities | View framing, courtyard, large deck, landscape rooms | Survey status; climate exposure; cut/fill; runoff outlet; roof/terrain/entry relationships |
| Arrival | Front door, understandable pedestrian route, coat/drop storage, door/weather protection | Generous daylit foyer, mudroom, seating, package space | Parked cars and doors do not obstruct entry; avoid long narrow tunnels |
| Parking | Needed number/type of spaces, driveway and pedestrian separation | Carport/garage, lift, EV, bicycle/ski/work storage | Vehicle and open-door envelopes, operator refuge, internal stair route, turning assumptions, floor levels |
| Living | Useful seating, daylight, privacy, circulation, media/storage decision | Fireplace, library, indoor/outdoor room, acoustics | Furniture use, glare, TV/fireplace heights, fireplace type/flue/clearances/air supply |
| Dining | Table, actual chairs, usable pullback and serving route | Larger entertaining table, banquette, outdoor counterpart | Occupied chairs and through route; lighting placement |
| Cooking | **Range OR cooktop + separate oven**, extraction hood/exhaust strategy, refrigerator/freezer, sink/faucet, dishwasher | Double ovens, steam oven, induction, additional prep sink | Entire equipment set; work/landing surfaces; open appliance doors; power/water/exhaust/service spaces |
| Kitchen storage | Dry-food pantry, cookware, dishes, cutlery, cleaning, waste/recycling | Walk-in pantry, appliance garage, scullery, beverage storage | Storage fronts open; bins are real provisions; no solid cabinet intersects oven/dishwasher |
| Refrigerator | Capacity and footprint for household; full access and service path | 42–48 in allowance, panel-ready fronts, separate refrigerator/freezer columns | Actual selected unit controls width/depth, ventilation, hinge swing, drawer removal, water and panels |
| Primary bedroom | Real bed, bedside provision, privacy/daylight, usable clothes storage | King layout, walk-in dressing, seating/view, private outdoor access | Bed sides/foot; wardrobe door/drawer operation; egress strategy pending local verification |
| Other bedrooms | Bed, usable **modeled clothes storage**, daylight, privacy, reachable bath | Desks, ensuite baths, flexible guest/work use | Do not omit storage because a local legal definition might allow it; check furniture and escape strategy |
| Primary bathroom | Bathing, toilet, vanity/storage, ventilation, privacy, towel space | **Two basins, separate shower, separate tub, enclosed WC** for premium briefs | Replan/enlarge to fit; comfortable dry circulation, door conflicts, counter space, mirror/light, cleaning |
| Other bathrooms | Usable fixtures, dry standing area, storage and exhaust | Additional shower/tub as household needs; powder near public rooms | Door privacy, cleaning reach, accessible/future needs; do not count a toilet room as a whole extra bath |
| Laundry | Washer/dryer, door space, detergent, baskets, folding and service | Sink, drying rack, hanging, distributed laundry | Water/leak/drain provisions; dryer ventilation or condensate; vibration/acoustic separation |
| General storage | Linen, broom/vacuum, cleaning, luggage/seasonal, household supplies | Built-ins, dedicated gear/storage rooms | Assign locations; do not label an inaccessible leftover void as storage |
| Building services | HVAC, fresh air, hot water, plumbing/electrical spaces, service routes | Zoning, filtration, efficient heat pumps, solar/battery, recirculation | Separate modeled allowances from selected/sized equipment; replacement paths, noise, drains |
| Lighting | Ambient, task, mirrors, circulation, exterior entry, controls | Recessed base, wall wash, discreet task strips, selected statement fixtures | Real apertures for recessed housings; glare, ceiling layout, beam/output and dimming unresolved until selected |
| Hardware | Door operation/latching/privacy, cabinet access, finishes | Shared knob/pull/edge-pull/lever families; coordinated finish palette | Correct mounting face, hand clearance, projection, swing conflicts, rebates for recessed hardware |
| Outdoor living | Thresholds, drainage, usable furniture, shade/privacy decision | Deck, balcony, pergola, patio, outdoor kitchen, shower/pool | Support/guards, furniture use, waterproofing, stair/grade access, wildfire/corrosion/exposure |
| Resilience / future | Locally appropriate moisture, wind, snow, fire, safety, energy and maintenance strategy | Backup power, adaptable room, future mobility, added conduits | Site/product/professional evidence; do not use a prestige material as a substitute for performance |

## Options are not mandatory upgrades

Record decisions on fireplace type/location, bathtub in secondary baths, second dishwasher, wine/beverage refrigeration, scullery, gym/game room, office, guest suite, elevator/lift, sauna, pool/spa, outdoor kitchen, extra garage, smart controls and automated shades. Choose based on household, site, budget, maintenance and room quality. The answer can be "excluded" with a reason.

For selected game rooms, check the actual activity envelope as well as the furniture footprint: pool-table dimensions, intended cue length and player stance, unobstructed shots, seating/stair circulation, delivery path, lighting, HVAC and noise. Follow [interior operation guidance](design-guide/interiors-storage-access.md).

## Library selection and contribution

1. Read the [visual catalog](../library/README.md) and search exact `asset.json` manifests. Select compatible dimensions, origin, installation and clearance assumptions—not only appearance.
2. Link the chosen version. Place it at correct real-world scale. Do not scale an appliance or cabinet arbitrarily to make an unresolved plan fit.
3. If adaptation is necessary, create a new version of the same asset for a compatible revision, or a clearly named new asset for a distinct option. Preserve the adopted source unchanged; record `derived_from`, the reason, dimensions, interfaces, licenses and generator.
4. Publish the reusable result with editable source/generator, dependencies and an actual native preview. Reopen it and inspect it installed in a host home. Then record adoption in the home's manifest and asset-use schedule. See [full contribution workflow](assets.md).
5. A bespoke layout can remain local. Repeated generic plants, paving, hardware, lights, cabinets and appliances should not remain hidden in a house generator.

## Evidence and review

Before final output promotion, inspect a furnished plan, front arrival, rear living, side/roof/site view and relevant interior views. Recheck every affected schedule after a layout change. Record concept checks separately from manufacturer selection, structural/MEP calculations, jurisdictional approvals and field verification. See the sourced [tier research](research/home-program-tiers.md), [kitchen/bath decisions](research/kitchen-bath-tiers.md) and [roof/climate matrix](research/roof-climate-materials.md).
