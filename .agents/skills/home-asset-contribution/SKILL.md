---
name: home-asset-contribution
description: Select, adapt, publish, and adopt reusable architectural assets in this repository's versioned library. Use for shared materials, plants, paving, cabinetry, fixtures, hardware, lighting, appliances, or furnishings; keep genuinely site-specific terrain and home layouts local.
---

# Home asset contribution

Paths below are relative to the repository root, three levels above this skill folder. Read [docs/assets.md](../../../docs/assets.md), applicable `library/AGENTS.md` files and the adopting home's guidance. The canonical asset workflow controls packaging and review; do not create a competing manifest convention.

## Choose reuse or contribution

Search [the visual catalog](../../../library/README.md) and `library/**/asset.json` before modeling. Inspect candidate dimensions, origin/front direction, mounting, operating/service clearances, allowed scaling, material dependencies and rights. Choose for installation fit as well as appearance.

- Suitable existing option: link its exact published collection/material version using repository-relative paths.
- Compatible revision of the same component: preserve the adopted version and publish the next version.
- Distinct size, type or option that should coexist: create a descriptive new slug and record derivation.
- Bespoke site geometry or one-off layout: retain locally with a reason in the home's schedule.

Confirm the proposed parent actually exists. If a requested source size/version is missing, identify the nearest real source and record that derivation truthfully, or create a new original asset; never invent an upstream asset.

Do not shrink standard appliances to conceal layout problems. A copied generator or local mesh is not library adoption; shared materials alone do not share repeated object geometry.

## Package the asset

Use `library/<category>/<slug>/vNNN/`. Follow nearby manifests and existing authoring helpers. Include stable ID/version, meter dimensions, Z-up placement origin, front direction/axes, mounting interfaces, permitted variation/scaling, operating and service clearance assumptions, exact dependencies, source/generator, authorship and redistribution rights.

For a variation, record `derived_from` with original ID/version, changed interfaces and rationale; retain upstream attribution and compatible licensing. Keep adopted versions immutable. Distinguish original concept equipment from commercially specified products. An unresolved installation requirement belongs in the manifest and host decision record, not an invented performance claim.

Keep dependencies portable. Use local relative texture paths and pinned library links. Include an actual native preview; never substitute an unrelated image. Avoid adding restricted third-party source files to the public repository.

## Verify, adopt and expose

Reopen the asset in a fresh authoring process. Inspect dimensions, origin, orientation, missing dependencies, geometry and materials in isolation. Install it in the intended host and check mounting, openings/recesses, door/drawer operation, surrounding clearances and service space as applicable. An asset preview alone cannot validate host integration. Closed geometry does not prove operating clearance: record the open-state angle/travel, required envelope, basis (measured geometry, manufacturer or concept assumption), and whether the host was actually checked.

Explicitly adopt the reviewed version in the home's native model, `project.json` and `assets/README.md`; record checks and deliberate bespoke exceptions. Update affected plans/images and the visual library catalog after actual inspection. Show which home uses it: an unused file proves availability, not reuse.

For missing metadata or rights, leave the candidate unresolved rather than inventing values. Preserve existing artifacts and report blockers. This workflow does not authorize unrelated downloads, purchases, commits or publication.
