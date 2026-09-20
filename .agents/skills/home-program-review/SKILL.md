---
name: home-program-review
description: Resolve or review a home concept's program, layout, equipment, storage, circulation, and site relationships in this repository. Use before new layouts or substantial home revisions, and when checking missing features; a cosmetic render-only change does not require a whole-home redesign.
---

# Home program review

Use this repository's maintained checklist rather than inventing a fresh definition of a complete home. Paths below are relative to the repository root, three levels above this skill folder.

## Establish the brief

Read the root and target home's guidance, its brief and existing decisions, then [home-design-standard.md](../../../docs/home-design-standard.md) and [home-program-checklist.md](../../../docs/home-program-checklist.md). Preserve explicit user choices. Record household, tier, site/climate evidence, assumptions, story count, parking, area convention and priorities in `homes/<slug>/program.md`, starting from [the program template](../../../templates/home/program.md) when missing.

Tier describes choices, not permission to omit baseline function. Apply this user's premium defaults when that profile is adopted by the actual brief; compact or different briefs may need explicit alternatives. Record reasoned exceptions rather than cramming features into unusable spaces; do not generalize them to all homes. A real product, climate or jurisdiction can change the answer.

## Resolve applicable decisions

Use [the handbook index](../../../docs/design-guide/README.md) to load only relevant chapters: kitchens/baths for equipment and fixture arrangements; interiors for storage and operation; site/arrival for parking and hillside access; envelope/roof research for openings and climate; systems for services; buildability for interfaces and evidence.

For applicable features record required/optional/excluded, location, measured dimensions and operating clearances, evidence status, asset ID/version or justified bespoke work, and open decisions. Inventory `library/**/asset.json` before choosing components. Use the asset contribution workflow when a reusable option is missing.

Review the actual furnished plan and native model, not labels alone. Trace arrival with parked cars, garage-to-house access, daily room routes and outdoor exits. Check every bedroom's usable storage; the complete cooking/refrigeration/extraction set; bath privacy and fixture operation; laundry/general storage; lighting/hardware; service access; stairs, deck supports and roof/site runoff where applicable. Coordinate space before adding decorative detail.

Use the [interior decision cards](../../../docs/design-guide/interiors-storage-access.md) to record the actual headboard-to-wall relationship, each bathroom opening's hinge/swing or pocket strategy, WC proportions and plan legibility, and premium walk-in contents and operation. Use [large-pantry guidance](../../../docs/research/kitchen-bath-tiers.md#large-pantries-and-butlers-pantries) when a substantial pantry is allocated. Inspect a person using the basin, dressing storage or pantry counter with doors/drawers open: collision-free furniture bounding boxes do not prove usable standing space. A bed count, closed-storage aisle or room label is insufficient evidence.

Apply the handbook's [spatial placement review](../../../docs/design-guide/interiors-storage-access.md#spatial-placement-compose-the-room-before-placing-assets) to the empty space between objects as well as their footprints. Explain why freestanding fixtures belong in their positions; check tub/filler/shower composition, dry approach and cleaning gaps rather than accepting objects scattered through a large room.

For bathroom openings, apply [daylight-with-privacy guidance](../../../docs/design-guide/interiors-storage-access.md#bathroom-windows-daylight-with-privacy). Record intended outlook, occupant positions, plausible exterior sightlines, day/night privacy, glazing/screen/shade choice and control/cleaning access. Verify that windows support fixture placement rather than forcing an awkward tub, missing mirror or exposed toilet. Distinguish assumed site privacy from checked evidence. Size toilet rooms for privacy and use rather than excess empty space, and apply the brief's premium bidet-toilet preference with real product/service allowances.

For paneled integrated refrigeration, use the [flush-placement guidance](../../../docs/research/kitchen-bath-tiers.md#integrated-refrigerator-placement): check actual finished-front alignment, full-depth above-fridge cabinetry and full hinge/handle/drawer-removal operation beside return walls. Require a compatible unit/recess and documented filler/setback; neither a closed-box collision check nor a nominal counter-depth label establishes an integrated fit.

## Verify and record

Inspect front, rear, side/roof and relevant interior renders alongside current drawings. Record observed defects, measured checks, fixes and remaining decisions in `design-review.md`; update `program.md`, `project.json` and the asset-use schedule together.

Keep modeled geometry, dimensioned reservations, manufacturer selection, engineering, approval and field verification distinct. A route test is not accessibility approval. Open functional failures prevent a resolved review; unverified professional/site decisions remain explicit.

After layout changes, regenerate and inspect affected native/interchange files, plans and current outputs together. Follow existing output naming; do not create parallel history folders. Report what was actually checked and what remains unresolved. This skill grants no additional publishing authority.
