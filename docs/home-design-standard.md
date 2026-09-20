# What qualifies as a resolved home concept here

This is the repository's design standard, not a jurisdiction's legal definition, building-code approval, engineering specification, or permit checklist. Local rules and a real survey remain unverified until explicitly investigated. Older projects are legacy concepts until reviewed against this standard; adding this document does not certify them.

## Required program

- State the household assumptions, bedrooms, bathrooms, stories, parking, gross/conditioned area convention, and outdoor living program before modeling.
- Every bedroom has a real bed layout, usable clothes storage, an accessible storage front, privacy, daylight and a plausible emergency-egress strategy to be checked locally. Show closets/wardrobes with depths and doors; a room label is insufficient.
- Include practical kitchen work zones, food storage, laundry, linen/general storage, coat/drop storage, mechanical/service space and waste handling. Mark unresolved equipment/service provisions explicitly.
- Include parking and an arrival route when the brief implies vehicular access. If intentionally car-free, record that decision rather than omitting it accidentally.

## People and movement

- Trace road → parking → sheltered entrance → coat/drop zone → public living area. Keep pedestrian routes usable while cars are parked. Design a welcoming foyer with daylight and a view toward public space; avoid an unnecessary long narrow corridor between blank walls.
- Trace bedroom → bathroom, garage → house, kitchen → dining, interior → deck/patio, and every stair connection. Keep these paths free with doors, chairs and storage in ordinary use.
- Check furniture-scale dimensions, chair pullback, bed sides/end, wardrobe door/drawer operation, appliance openings and bathroom privacy. Record actual dimensions, not only a blanket pass/fail minimum.
- Compose fixtures and furniture with walls, windows and activity zones. Reject accidental floating placement and awkward leftover gaps, including freestanding tubs that crowd the shower approach. Verify useful negative space and cleaning access in plan and eye-level views; follow [spatial placement guidance](design-guide/interiors-storage-access.md#spatial-placement-compose-the-room-before-placing-assets).
- Place beds at deliberate headboard walls; resolve each bathroom door's hinge/swing or pocket individually. Design large pantries and premium walk-ins as usable working/dressing rooms, not sparse oversized labels. Apply the detailed [interior operation guidance](design-guide/interiors-storage-access.md) and [pantry decisions](research/kitchen-bath-tiers.md#large-pantries-and-butlers-pantries).
- Stairs need a real opening, consistent treads/risers, landings, headroom and guards. Decks need modeled support logic, guards and access. Avoid impossible cantilevers or inaccessible leftover rooms.

## Site and envelope

- Show front/road, side, rear, roof and outdoor living relationships consistently. Parking, garage doors, front door and walkout exits must appear in the model and plan where included in the brief.
- Draw slope and floor datums; use an actual terrain model, plausible cut/fill/retaining strategy, and a usable landing outside a walkout. Do not bury windows, float patios or put trees through floors.
- Resolve actual roof slopes, runoff direction, collection and discharge concept together; demonstrate these in roof plans/sections even where the slope is not prominent in elevation. Product minimums, structural/snow/wind loads, drainage capacity, waterproofing and coastal corrosion details remain professional/site-specific checks.

## Asset reuse and publication gates

1. Inventory materials, plants, paving, storage, fixtures and furniture before generation. Reuse suitable pinned library versions; publish missing repeated components with source, dimensions, origin, rights and dependencies.
2. Record actual adoption in `project.json` and `assets/README.md`; verify native relative links reopen on disk. Bespoke layouts and terrain can remain home-specific, but repeated generic objects belong in the library.
3. Inspect a furnished plan and real rendered front/rear/side views. Record defects and fixes in `design-review.md`, distinguishing checked concept geometry from unverified engineering or regulations.
4. Update the native scene, interchange file, plans, current output gallery and README together after layout changes. Do not publish new renders of an obsolete plan.

The review should answer: would a person understand where to arrive, park, enter, store belongings, cook, sleep, bathe and move outdoors—and do the files actually show those provisions?
