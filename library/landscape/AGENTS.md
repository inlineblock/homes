# Reusable landscape assets

- Look here before creating plants inside a home generator. Repeated grass clumps, shrubs, trees and rocks must be library collections with a pinned version, not independently regenerated meshes in each home.
- Place instances at the actual local terrain height. Check the rendered base: floating stems and buried canopies fail review. Preserve a clear pedestrian route, driveway and sightlines.
- Use restrained scale and rotation variation for plants. Record nominal size and the placement origin. A generic ornamental asset is not a botanical or climate suitability specification.
- Publish genuinely different geometry as another asset or version; do not clone the same mesh under a new home-specific name. New plant assets need original-source information, dimensions, a real rendered preview and a native reopen check.
- `tools/common/shared_assets.py` exposes grass, shrub and olive collections. Mountain conifer has its own generator and can be mixed with these understory assets where appropriate.

## Expansion and selection

- Read [the plant library](README.md), [native gallery](gallery.md) and [catalog](catalog.json) for the six existing families and 35 new families / 105 named variants. Read each actual manifest and validation receipt before pinning a dependency; modeled, visually reviewed and adopted are distinct statuses.
- Make species and growth forms visually distinct; do not relabel generic grass/shrub/tree meshes or swap fruit colors to claim new botanical families. Preserve named cultivar/rootstock differences where they affect form.
- Record modeled size separately from expected mature spread, and distinguish young, container-grown, pruned and dwarf-rootstock forms. Use coherent seasonal states and several reviewed branch arrangements to reduce repetition.
- Choose plants for the actual climate/site. Mountain, desert, water-wise, coastal and suburban are browse tags, not universal suitability claims; distinguish coastal salt spray from inundation and protected garden exposure.
- Each new family needs native whole-plant and detail previews, ground-contact/scale checks and a reviewed host placement before claiming adoption. Follow the plan and parent asset workflow for metadata and publication.

## Native models and evidence

- The seven family builders and shared mesh helper live in `tools/library/plants/`; follow [their workflow](../../tools/library/plants/README.md). Use the actual `blender.variants[].collection` name from the pinned manifest. Never copy a scene-wide stack of overlapping variant collections into a home.
- Whole-family triptychs and close details are native renders. Keep both current after geometry changes; an Image Gen result cannot validate botanical mesh detail or substitute for these previews.
- The [comparative nursery](nursery/README.md) links one variant from each new family into separate demonstration beds. It checks origin, spacing, clear paths and relative links; it is neither a universal mixed-climate planting scheme nor adoption into an existing home.
- Rebuild and reopen the nursery after source geometry changes so its bounds and source hashes stay current. Once an asset version is committed or adopted, preserve it and publish a reviewed new version.
- Several Blender background processes may build independent families concurrently. Give each process its own file ownership and low CPU thread count; serialize GPU preview jobs to avoid competing for shared memory. Never write the same native file from two agents.
