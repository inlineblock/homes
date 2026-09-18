# Mountain House design review

This is an architectural concept and furnished visualization. The review below separates demonstrated model behavior from product selection, engineering and permit work. The site is original illustrative terrain, not a surveyed parcel.

## Brief and layout

- Two levels total: main living/garage at the front road and a lower rear walkout. No third floor or occupied room beneath the garage.
- Three modeled bedrooms, each with linked usable clothes-storage modules: 8 linear feet in the primary dressing room and 6 feet in each lower bedroom. These are repository design requirements, not a statement that closets universally define legal bedrooms.
- Primary suite has two basins, a separate shower and tub, and an enclosed toilet room. The guest bath and powder room complete the assumed 2.5-bath program.
- The foyer is eight feet nominally wide, with separate garage/mudroom arrival and coat/drop provision. Living/dining faces the forest. Kitchen contains cooktop, oven, hood, dishwasher, sink, pantry, waste/recycling and cabinet-matched 48-inch refrigeration.
- The 60 x 14 ft rear deck and 8 x 36 ft side return provide 1,128 sq ft of outdoor floor, excluded from enclosed area. Pergola, glass guards, posts and knee braces are visible concepts. The lower patio receives shade; the deck is not a verified waterproof roof.

## Measured native evidence

`model/model-validation.json` records fresh-file checks of 4,104 sq ft gross enclosed floor, 3,528 sq ft conditioned gross after excluding the 576 sq ft garage, three bed frames, actual stair opening and 20 equal 6.6-inch rises with 11-inch treads. The footprint calculation includes walls; it is not net usable living area.

Thirteen sampled routes were checked against evaluated furniture, linked asset bounds, walls and doors using a 30-inch swept diameter. These cover arrival, garage/mudroom, primary bed/dressing/bath/shower/WC, rear deck access, lower stair arrival, lower bedrooms and kitchen working aisle. They demonstrate the named concept paths only; they do not establish accessibility, minimum code clearances, every intermediate door position or all simultaneous appliance operations. The refrigerator was shifted nine inches toward the side wall, reserving more than six inches between its conceptual left 90-degree door-swing line and the island end. Product-specific articulation, service space and simultaneous refrigerator/oven/dishwasher/wardrobe operation remain selection checks.

`model/asset-adoption.json` checks exact manifest/native dependency agreement and actual scene use rather than merely loaded libraries. Relative paths stay within this checkout. The asset schedule identifies bespoke geometry and reusable components still needing library promotion.

`model/source-validation.json` records an isolated rebuild and fresh reopen: all 3,942 objects, geometry/transforms, cameras/lights/render settings, 24 library versions and asset placements match. Three WC instances use different organizational collections between the saved model and generator; geometry and appearance are identical. The build includes the chaise supports and refrigerator offset.

## Visual review

Actual native drafts were inspected for front arrival, rear/deck/patio relationship, side slope, kitchen and primary bathroom. A second agent reviewed front, deck, side and both plans. This identified and prompted correction of the road-to-entry paving gap, the bare distant terrain horizon and stale plan furniture. Primary side glazing was moved wholly into the bedroom after the suite replan; bath surfaces, recessed basins and lighting were refined. Close-up review also led to solid chaise supports down to the patio and the refrigerator door-swing correction. Final output verification is recorded in `model/output-validation.json`, including image hashes, per-view sample settings and booklet page review.

## Explicit unresolved design work

- Survey, solar orientation, geotechnical/retaining strategy, slope stability, cut/fill and drainage; road/drive grade and vehicle turning at a real site.
- Structural sizes/connections for the hillside foundation, deck, glass guards, pergola, stair, garage span and roof; snow/wind/seismic loads and falling snow/ice at the front approach.
- A tested roof product appropriate to the 0.66:12 slope, continuous waterproofing/air/thermal assemblies, gutter fall/capacity and lawful discharge. Standing-seam appearance is not a roof-system specification.
- Bedroom egress windows and hardware, local fire separation/garage entry requirements, stair headroom/handrail/guard details and accessibility adaptation. These have not been certified.
- HVAC capacity/distribution, fresh-air supply/exhaust, service/replacement paths, electrical circuits/outlets/safety devices, water supply and lower-level waste connection. The service room reserves space, not an engineered system.
- Fireplace fuel/product, combustion/flue clearances and interaction with kitchen exhaust. The generic hood asset is a visualization envelope; island support, rear finish, capture performance and makeup air require a suitable selected assembly.
- Wet-room waterproofing, drains, non-slip materials, exact fixture rough-ins and service access; countertop/window threshold weather details; lighting photometry and controls.

The native scene, classified IFC and dimensioned plans must not be represented as construction documents or permit approval. Schema validation and a successful render do not resolve these items.

## Timber appearance correction

The earlier sunlit exterior rendered pale peach, with repeated soft grain and incorrect grain direction on several horizontal members. Mountain now explicitly adopts cedar v003 and thermo-ash v002. The revised original shaders use neutral brown colors, per-object growth samples and tone, fine irregular lines/pores, varied matte roughness and physical-meter UVs aligned along each member's longest local axis. The earlier shared versions remain immutable.

Two rounds of same-camera host studies and neutral material samples were inspected, including an independent reviewer. Bright and shaded wood now retain a brown identity; the second round added fine growth detail after the first still read as broad blurred stripes. Scene lighting, exposure and architectural geometry were preserved. `model/material-validation.json` records identical before/after geometry hashes and 2,153 mapped timber objects; the native reopen and exact 24-pin adoption check passed. Current final image/PDF evidence is in `model/output-validation.json`.
