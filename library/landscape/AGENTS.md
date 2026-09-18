# Reusable landscape assets

- Look here before creating plants inside a home generator. Repeated grass clumps, shrubs, trees and rocks must be library collections with a pinned version, not independently regenerated meshes in each home.
- Place instances at the actual local terrain height. Check the rendered base: floating stems and buried canopies fail review. Preserve a clear pedestrian route, driveway and sightlines.
- Use restrained scale and rotation variation for plants. Record nominal size and the placement origin. A generic ornamental asset is not a botanical or climate suitability specification.
- Publish genuinely different geometry as another asset or version; do not clone the same mesh under a new home-specific name. New plant assets need original-source information, dimensions, a real rendered preview and a native reopen check.
- `tools/common/shared_assets.py` exposes grass, shrub and olive collections. Mountain conifer has its own generator and can be mixed with these understory assets where appropriate.
