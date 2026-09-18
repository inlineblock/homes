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

## Verify and record

Inspect front, rear, side/roof and relevant interior renders alongside current drawings. Record observed defects, measured checks, fixes and remaining decisions in `design-review.md`; update `program.md`, `project.json` and the asset-use schedule together.

Keep modeled geometry, dimensioned reservations, manufacturer selection, engineering, approval and field verification distinct. A route test is not accessibility approval. Open functional failures prevent a resolved review; unverified professional/site decisions remain explicit.

After layout changes, regenerate and inspect affected native/interchange files, plans and current outputs together. Follow existing output naming; do not create parallel history folders. Report what was actually checked and what remains unresolved. This skill grants no additional publishing authority.
